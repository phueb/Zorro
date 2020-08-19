from typing import List, Dict

from babeval import configs
from babeval.vocab import get_vocab


def to_percentile(val: float):
    return int(val - (val % 10) + 10)


vocab = get_vocab()

# load bigrams
bigram2percentile = {}
bigram2f = {}
w2max_left_bigram_f = {}
w2max_right_bigram_f = {}
left_w2right_w2f = {}
right_w2_left_w2f = {}

with (configs.Dirs.root / 'word_lists' / 'bi-grams.txt').open() as f:
    for line in f.readlines():
        frequency, w1, w2, percent = line.split()
        frequency = int(frequency)
        bigram2percentile[(w1, w2)] = to_percentile(float(percent))
        bigram2f[(w1, w2)] = frequency
        #
        if frequency > w2max_left_bigram_f.setdefault(w1, 0):
            w2max_left_bigram_f[w1] = frequency
        if frequency > w2max_right_bigram_f.setdefault(w2, 0):
            w2max_right_bigram_f[w2] = frequency

        # TODO
        left_w2right_w2f.setdefault(w1, {})[w2] = frequency
        right_w2_left_w2f.setdefault(w2, {})[w1] = frequency

bigram_frequency_percentiles = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
    

def categorize_left_bigrams(sentences_out: List[List[str]],
                            mask_index: int,
                            ) -> Dict[int, int]:
    res = {k: 0 for k in bigram_frequency_percentiles}

    for sentence in sentences_out:
        bigram = (sentence[mask_index - 1], sentence[mask_index])
        try:
            percentile = bigram2percentile[bigram]
        except KeyError:
            percentile = 0

        assert percentile in bigram_frequency_percentiles
        res[percentile] += 1

    return res


def categorize_right_bigrams(sentences_out: List[List[str]],
                             mask_index: int,
                             ) -> Dict[int, int]:
    res = {k: 0 for k in bigram_frequency_percentiles}

    for sentence in sentences_out:
        bigram = (sentence[mask_index], sentence[mask_index + 1])
        try:
            percentile = bigram2percentile[bigram]
        except KeyError:
            percentile = 0

        res[percentile] += 1

    return res