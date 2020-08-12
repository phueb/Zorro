import numpy as np

from babeval.vocab import get_vocab, get_frequency
from babeval.bigrams import right_w2_left_w2f, left_w2right_w2f


class ReaderOpenEnded:
    def __init__(self, predictions_file_path):

        self.predictions_file_path = predictions_file_path
        self.sentences_in, self.sentences_out = self.get_columns()

        print(f'Initialized reader for open_ended predictions. Found {len(self.sentences_out)} lines in file.')

    @property
    def sentences_out_unigram_distribution_control(self):
        return self.get_sentences_out_unigram_distribution_control()

    @property
    def sentences_out_left_bigram_distribution_control(self):
        return self.get_sentences_out_left_bigram_distribution_control()

    @property
    def sentences_out_right_bigram_distribution_control(self):
        return self.get_sentences_out_right_bigram_distribution_control()

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

    def get_sentences_out_unigram_distribution_control(self):
        """
        :return: list of test sentences with MASK symbol replaced with random word from vocab
         sampled based on frequency in corpus
        """
        print('Making 1-gram distribution control')

        vocab = get_vocab()
        freq = get_frequency()
        weights = np.array(freq) / sum(freq)
        sampled_words = iter(np.random.choice(vocab, size=len(self.sentences_in), p=weights))

        result = []
        for s in self.sentences_in:
            assert '[MASK]' in s, s
            s_new = [next(sampled_words) if w == '[MASK]' else w for w in s]
            result.append(s_new)

        return result

    def get_sentences_out_left_bigram_distribution_control(self):
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

    def get_sentences_out_right_bigram_distribution_control(self):
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


class ReaderForcedChoice:
    def __init__(self, predictions_file_path):

        self.predictions_file_path = predictions_file_path
        self.sentences_in, self.cross_entropies = self.get_columns()

        print(f'Initialized reader for open_ended predictions. Found {len(self.sentences_in)} lines in file.')

        print()

    def get_columns(self):
        lines = self.predictions_file_path.open().readlines()

        col1 = []
        col2 = []
        for line in lines:
            parts = line.split()
            sentence_in = parts[:-1]
            xe = float(parts[-1])
            col1.append(sentence_in)
            col2.append(xe)

        return col1, col2