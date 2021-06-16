import random
from pathlib import Path
from typing import Dict, Tuple, List

from zorro.vocab import get_vocab_words, get_frequency
from zorro import configs


# precompute word frequency for baseline models
vocab_words = get_vocab_words(return_excluded_words=True)  # to change vocab_size, change configs.Data.vocab_size
frequencies = get_frequency(return_excluded_words=True,
                            corpus_name='total')
assert len(frequencies) == len(vocab_words)
w2f = {w: f for w, f in zip(vocab_words, frequencies)}


class DataExperimental:
    def __init__(self,
                 model_output_path: Path,
                 phenomenon: str,
                 paradigm: str,
                 ) -> None:
        """
        this class relies on order in original sentences file to correctly pair sentences,
        to correctly read experimental data.
        """

        # load ordered sentences - the only way to know which sentences are paired (answer: consecutive sentences)
        vocab_size = model_output_path.parent.name
        path = configs.Dirs.root / 'sentences' / vocab_size / f'{phenomenon}-{paradigm}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs: List[Tuple[List[str], List[str]]] = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2],
                                                                                    sentences_ordered[1::2])]

        # sentences at odd numbered lines are bad, and sentences at even numbered lines are good
        self.grammatical_scores: List[Tuple[bool, bool]] = [(False, True) for _ in self.pairs]

        # load unordered sentences to which cross entropies are assigned by to-be-evaluated model
        self.s2cross_entropies: Dict[Tuple[str], float] = self.make_s2cross_entropies(model_output_path)

    @staticmethod
    def make_s2cross_entropies(model_output_path: Path,
                               ) -> Dict[Tuple[str], float]:
        lines = model_output_path.open().readlines()

        res = {}
        for line in lines:
            parts = line.split()
            s = parts[:-1]
            xe = float(parts[-1])
            res[tuple(s)] = xe

        return res


class DataBaseline:
    def __init__(self,
                 group_name: str,
                 phenomenon: str,
                 paradigm: str,
                 ) -> None:
        """
        this class relies on order in original sentences file to correctly pair sentences,
        to produce baseline condition data.
        """

        self.group_name = group_name

        path = configs.Dirs.root / 'sentences' / configs.Data.vocab_name / f'{phenomenon}-{paradigm}.txt'
        sentences_ordered = [s.split() for s in path.open().read().split('\n')]
        self.pairs: List[Tuple[List[str], List[str]]] = [(s1, s2) for s1, s2 in zip(sentences_ordered[0::2],
                                                                                    sentences_ordered[1::2])]

        # sentences at odd numbered lines are bad, and sentences at even numbered lines are good
        self.grammatical_scores: List[Tuple[bool, bool]] = [(False, True) for _ in self.pairs]

        self.s2cross_entropies: Dict[Tuple[str], float] = self.make_cross_entropies_unigram_distribution_baseline()

    def make_cross_entropies_unigram_distribution_baseline(self):
        """
        assign lower cross entropy to sentences that have a higher sum of word frequencies
        """

        res = {}

        for s1, s2 in self.pairs:

            # note: we default to zero for words not in vocab - happens for contractions like "isn't"
            s1_fs = sum([w2f.get(w, 0) for w in s1])
            s2_fs = sum([w2f.get(w, 0) for w in s2])

            # if contrast is word order or contrasting word is equally frequent, chose randomly
            if s1_fs == s2_fs:
                if random.random() < 0.5:
                    res[tuple(s1)] = 0.0
                    res[tuple(s2)] = 1.0
                else:
                    res[tuple(s1)] = 1.0
                    res[tuple(s2)] = 0.0

            # assign lower x-e to sentence with higher frequency
            else:
                res[tuple(s1)] = 0.0 if s1_fs > s2_fs else 1.0
                res[tuple(s2)] = 0.0 if s2_fs > s1_fs else 1.0

        return res
