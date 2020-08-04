"""
#u: BERT gives [UNK] for predicted_prep_verb
#c: number agreement between targeted_noun and predicted_prep_verb
#f: number disagreement between targeted_noun and predicted_prep_verbs
#n: Predictions given by BERT are non-prep_verbs
"""
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
    "other")

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


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        template2sentences_out.setdefault(templates[0], []).append(s2)
        if templates[0] not in template2mask_index:
            template2mask_index[templates[0]] = s1.index('[MASK]')
    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]], mask_index: int):
    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]  # predicted word may not be a copula ("is", "are")
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

        # other
        else:
            res['other'] += 1

    return res


def print_stats(sentences):
    print('Done')
