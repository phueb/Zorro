from typing import List

from babeval import configs


def to_percentile(val: float):
    return int(val - (val % 10) + 10)


# load bigrams
bigram2percentile = {}
with (configs.Dirs.root / 'word_lists' / 'bi-grams.txt').open() as f:
    for line in f.readlines():
        frequency, w1, w2, percent = line.split()
        bigram2percentile[(w1, w2)] = to_percentile(float(percent))

bigram_frequency_percentiles = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
    

def categorize_left_bigrams(sentences_out: List[List[str]], mask_index: int):
    res = {k: 0 for k in bigram_frequency_percentiles}

    for sentence in sentences_out:
        bigram = (sentence[mask_index - 1], sentence[mask_index])
        try:
            percentile = bigram2percentile[bigram]
        except KeyError:
            percentile = 0

        res[percentile] += 1

        print(bigram)
        print(percentile)




    return res
