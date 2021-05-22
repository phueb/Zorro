import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

from zorro.vocab import get_vocab_words, get_frequency
from zorro import configs


# precompute word frequency for baseline models
vocab_size2w2p = {}
for control_name in configs.Data.control_names:
    vocab_size = control_name.split()[0]
    vocab_words = get_vocab_words(configs.Data.vocab_name_template.format(vocab_size),
                                  return_excluded_words=True)
    freq = get_frequency(configs.Data.vocab_name_template.format(vocab_size),
                         return_excluded_words=True)
    assert len(freq) == len(vocab_words)
    unigram_probabilities = np.array(freq) / sum(freq)
    vocab_size2w2p[control_name] = {w: p for w, p in zip(vocab_words, unigram_probabilities)}


class DataExperimental:
    def __init__(self,
                 predictions_file_path: Path,
                 phenomenon: str,
                 paradigm: str,
                 ) -> None:
        """
        control condition data in the forced-choice setting relies on ordered data in
        sentences/forced-choice where sentence pairs are guaranteed to be in consecutive lines.
        this means, this class relies on order in original sentences file to correctly pair sentences,
        to correctly read experimental data.
        """

        # load ordered sentences - the only way to know which sentences are paired (answer: consecutive sentences)
        vocab_size = predictions_file_path.parent.name
        print(f'Loading test sentences with vocab size={vocab_size}')
        path = configs.Dirs.root / 'sentences' / vocab_size / f'{phenomenon}-{paradigm}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2], sentences_ordered[1::2])]

        # load unordered sentences to which cross entropies are assigned by to-be-evaluated model
        self.s2cross_entropies = self.make_s2cross_entropies(predictions_file_path)

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


class DataControl:
    def __init__(self,
                 group_name: str,
                 phenomenon: str,
                 paradigm: str,
                 ) -> None:
        """
        control condition data in the forced-choice setting relies on ordered data in
        sentences/forced-choice where sentence pairs are guaranteed to be in consecutive lines.
        this means, this class relies on order in original sentences file to correctly pair sentences,
        to produce control condition data.
        """

        self.group_name = group_name
        self.vocab_size = group_name.split()[0]

        print(f'Loading test sentences with vocab size={vocab_size}')
        path = configs.Dirs.root / 'sentences' / str(self.vocab_size) / f'{phenomenon}-{paradigm}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2],  # odd numbered: bad sentences
                                                 sentences_ordered[1::2])  # even numbered: good sentences
                      ]

        self.s2cross_entropies = self.make_cross_entropies_unigram_distribution_control()

    def make_cross_entropies_unigram_distribution_control(self):

        res = {}

        w2p = vocab_size2w2p[self.group_name]

        nas = (configs.Dirs.external_words / "nouns_ambiguous_number.txt").open().read().split()

        for s1, s2 in self.pairs:
            for w1, w2 in zip(s1, s2):
                if w1 != w2:
                    if w2p[w1] > w2p[w2]:
                        xe1, xe2 = 0.0, 1.0
                    else:
                        xe1, xe2 = 1.0, 0.0
                    break
            else:
                for w in s1:
                    if w in nas:
                        break
                else:
                    raise RuntimeError('Sentence Pair has identical sentences')

            res[tuple(s1)] = xe1
            res[tuple(s2)] = xe2

        return res
