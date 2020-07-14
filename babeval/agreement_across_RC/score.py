from pathlib import Path
from typing import List

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

templates = ['default',
             ]

prediction_categories = (
    "non-start\nword-piece\nor\n[UNK]",
    "correct\ncopula",
    "false\ncopula",
    "non-copula",
)

# load word lists
nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split("\n")

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

nouns_singular += ['one', '[NAME]']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)

mask_index = -3


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    res = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        res.setdefault(templates[0], []).append(s2)
    return res


def categorize_predictions(sentences_out: List[List[str]]):
    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        targeted_noun = sentence[1]

        # [UNK]
        if predicted_word.startswith('##') or predicted_word == "[UNK]":
            res["non-start\nword-piece\nor\n[UNK]"] += 1

        # correct copula
        elif targeted_noun in nouns_plural and predicted_word in copulas_plural:
            res["correct\ncopula"] += 1

        elif targeted_noun in nouns_singular and predicted_word in copulas_singular:
            res["correct\ncopula"] += 1

        # false copula
        elif targeted_noun in nouns_plural and predicted_word in copulas_singular:
            res["false\ncopula"] += 1

        elif targeted_noun in nouns_singular and predicted_word in copulas_plural:
            res["false\ncopula"] += 1

        # Non-copula
        else:
            res["non-copula"] += 1

    return res


def print_stats(sentences):
    print('Done')
