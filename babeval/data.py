import numpy as np
from pathlib import Path
import random
from typing import List, Dict, Tuple

from babeval.whole_words import get_whole_words, get_frequency
from babeval.bigrams import right_w2_left_w2f, left_w2right_w2f
from babeval import configs

whole_words = get_whole_words()
freq = get_frequency()
unigram_probabilities = np.array(freq) / sum(freq)
w2p = {w: p for w, p in zip(whole_words, unigram_probabilities)}



class DataExpOpenEnded:
    def __init__(self, predictions_file_path: Path):
        """
        reads experimental data from predictions file produced by model to--be-evaluated
        """

        self.predictions_file_path = predictions_file_path
        self.sentences_in, self.sentences_out = self.get_columns()

        print(f'Initialized reader for experimental open_ended predictions. '
              f'Found {len(self.sentences_out)} lines in file.')

    def get_columns(self):
        lines = self.predictions_file_path.open().readlines()

        col1 = [[]]
        col2 = [[]]
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                col1[-1].append(parts[0])
                col2[-1].append(parts[1])
            else:
                col1.append([])
                col2.append([])

        if not col1[-1]:
            del col1[-1]
        if not col2[-1]:
            del col2[-1]

        return col1, col2


class DataCtlOpenEnded(DataExpOpenEnded):
    def __init__(self,
                 predictions_file_path: Path,
                 control_name: str) -> None:
        """
        generate control (ctl) data for requested task
        """

        super().__init__(predictions_file_path)
        self.predictions_file_path = predictions_file_path
        self.sentences_in, _ = self.get_columns()

        if control_name == configs.Data.control_name_1gram:
            self.sentences_out = self.make_sentences_out_unigram_distribution_control()
        elif control_name == configs.Data.control_name_left_2gram:
            self.sentences_out = self.make_sentences_out_left_2gram_distribution_control()
        elif control_name == configs.Data.control_name_right_2gram:
            self.sentences_out = self.make_sentences_out_right_2gram_distribution_control()
        else:
            raise AttributeError('Invalid arg to "control_name".')

        print(f'Initialized reader for control open_ended predictions. '
              f'Found {len(self.sentences_out)} lines in file.')
        print()

    def make_sentences_out_unigram_distribution_control(self):
        """
        :return: list of test sentences with MASK symbol replaced with random word from whole_words
         sampled based on frequency in corpus
        """
        print('Making 1-gram distribution control')

        sampled_words = iter(np.random.choice(whole_words, size=len(self.sentences_in), p=unigram_probabilities))

        result = []
        for s in self.sentences_in:
            assert '[MASK]' in s, s
            s_new = [next(sampled_words) if w == '[MASK]' else w for w in s]
            result.append(s_new)

        return result

    def make_sentences_out_left_2gram_distribution_control(self):
        """
        :return: list of test sentences with MASK symbol replaced with random word from bigram distribution
         sampled based on frequency in corpus
        """
        print('Making left 2-gram distribution control')

        result = []
        for s in self.sentences_in:
            left_word = s[s.index('[MASK]') - 1]
            choices, fs = zip(*[(rw, f) for rw, f in left_w2right_w2f[left_word].items()])
            weights = np.array(fs) / sum(fs)
            s_new = [np.random.choice(choices, p=weights) if w == '[MASK]' else w for w in s]
            result.append(s_new)

        return result

    def make_sentences_out_right_2gram_distribution_control(self):
        """
        :return: list of test sentences with MASK symbol replaced with random word from bigram distribution
         sampled based on frequency in corpus
        """
        print('Making right 2-gram distribution control')

        # pre-computation
        choices_p, fs_p = zip(*[(lw, f) for lw, f in right_w2_left_w2f['.'].items()])
        weights_p = np.array(fs_p) / sum(fs_p)
        sampled_words_p = iter(np.random.choice(choices_p, size=len(self.sentences_in), p=weights_p))
        print('Finished pre-computation')

        result = []
        for s in self.sentences_in:
            right_word = s[s.index('[MASK]') + 1]
            if right_word == '.':  # do not compute this at each loop iteration
                sampled_word = next(sampled_words_p)
            else:
                choices, fs = zip(*[(lw, f) for lw, f in right_w2_left_w2f[right_word].items()])
                weights = np.array(fs) / sum(fs)
                sampled_word = np.random.choice(choices, p=weights)
            s_new = [sampled_word if w == '[MASK]' else w for w in s]
            result.append(s_new)

        return result


class DataExpForcedChoice:
    def __init__(self,
                 predictions_file_path: Path,
                 task_name: str) -> None:
        """
        contrary to open-ended reader, control condition data in the forced-choice setting relies on ordered data in
        sentences/forced-choice where sentence pairs are guaranteed to be in consecutive lines.
        this means, this class relies on order in original sentences file to correctly pair sentences,
        to correctly read experimental data.
        """

        # load ordered sentences - the only way to know which sentences are paired (answer: consecutive sentences)
        path = configs.Dirs.root / 'sentences' / 'forced_choice' / f'{task_name}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2], sentences_ordered[1::2])]

        # load unordered sentences to which cross entropies are assigned by to-be-evaluated model
        self.s2cross_entropies = self.make_s2cross_entropies(predictions_file_path)

        print(f'Initialized reader for forced-choice experimental predictions.'
              f'Found {len(self.s2cross_entropies)} lines in file.')
        print()

    @staticmethod
    def make_s2cross_entropies(predictions_file_path: Path,
                               ) -> Dict[Tuple[str], float]:
        lines = predictions_file_path.open().readlines()

        res = {}
        for line in lines:
            parts = line.split()
            s = parts[:-1]
            xe = float(parts[-1])
            res[tuple(s)] = xe

        return res


class DataCtlForcedChoice:
    def __init__(self,
                 control_name: str,
                 task_name: str,
                 ) -> None:
        """
        contrary to open-ended reader, control condition data in the forced-choice setting relies on ordered data in
        sentences/forced-choice where sentence pairs are guaranteed to be in consecutive lines.
        this means, this class relies on order in original sentences file to correctly pair sentences,
        to produce control condition data.
        """

        # load ordered sentences - the only way to know which sentences are paired (answer: consecutive sentences)
        path = configs.Dirs.root / 'sentences' / 'forced_choice' / f'{task_name}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2], sentences_ordered[1::2])]

        if control_name == configs.Data.control_name_1gram:
            self.s2cross_entropies = self.make_cross_entropies_unigram_distribution_control()
        elif control_name == configs.Data.control_name_left_2gram:
            self.s2cross_entropies = self.make_cross_entropies_left_2gram_distribution_control()
        elif control_name == configs.Data.control_name_right_2gram:
            self.s2cross_entropies = self.make_cross_entropies_right_2gram_distribution_control()
        else:
            raise AttributeError('Invalid arg to "control_name".')

        print(f'Initialized reader for forced-choice control predictions.'
              f'Found {len(self.s2cross_entropies)} lines in file.')
        print()

    def make_cross_entropies_unigram_distribution_control(self):
        print('Making 1-gram distribution control')

        res = {}

        for s1, s2 in self.pairs:
            for w1, w2 in zip(s1, s2):
                if w1 != w2:
                    if w2p[w1] > w2p[w2]:
                        xe1, xe2 = 0.0, 1.0
                    else:
                        xe1, xe2 = 1.0, 0.0
                    break
            else:
                raise RuntimeError('Sentence Pair has identical sentences')

            res[tuple(s1)] = xe1
            res[tuple(s2)] = xe2

        return res

    def make_cross_entropies_left_2gram_distribution_control(self):
        print('Making left 2-gram distribution control')

        res = {}

        for s1, s2 in self.pairs:
            assert len(s1) == len(s2)
            for i in range(len(s1)):
                if s1[i] != s2[i]:
                    left_word = s1[i - 1]  # left word may not exist
                    right_w2f = left_w2right_w2f[left_word]
                    bigram_f1 = right_w2f.get(s1[i], 0)
                    bigram_f2 = right_w2f.get(s2[i], 0)

                    if bigram_f1 > bigram_f2:
                        xe1, xe2 = 0.0, 1.0
                        # print((left_word, s1[i]), (left_word, s2[i]))  # TODO still testing
                        # print(bigram_f1, bigram_f2)
                    elif bigram_f1 < bigram_f2:
                        xe1, xe2 = 1.0, 0.0
                        # print((left_word, s1[i]), (left_word, s2[i]))
                        # print(bigram_f1, bigram_f2)
                    else:  # force guess
                        xe1, xe2 = random.sample([1.0, 0.0], k=2)
                    break
            else:
                raise RuntimeError('Sentence Pair has identical sentences')

            res[tuple(s1)] = xe1
            res[tuple(s2)] = xe2

        return res

    def make_cross_entropies_right_2gram_distribution_control(self):
        print('Making right 2-gram distribution control')

        res = {}

        for s1, s2 in self.pairs:
            assert len(s1) == len(s2)
            for i in range(len(s1)):
                if s1[i] != s2[i]:
                    right_word = s1[i + 1]  # right word may not exist
                    left_w2f = right_w2_left_w2f[right_word]
                    bigram_f1 = left_w2f.get(s1[i], 0)
                    bigram_f2 = left_w2f.get(s2[i], 0)
                    if bigram_f1 > bigram_f2:
                        xe1, xe2 = 0.0, 1.0
                    elif bigram_f1 < bigram_f2:
                        xe1, xe2 = 1.0, 0.0
                    else:  # force guess
                        xe1, xe2 = random.sample([1.0, 0.0], k=2)
                    break
            else:
                raise RuntimeError('Sentence Pair has identical sentences')

            res[tuple(s1)] = xe1
            res[tuple(s2)] = xe2

        return res