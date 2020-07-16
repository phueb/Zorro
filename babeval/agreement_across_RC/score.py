from pathlib import Path
from typing import List

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

templates = [
    'object-relative',
    'subject-relative',
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


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        if s1[4] in {'like', 'likes'}:
            template2sentences_out.setdefault(templates[0], []).append(s2)
            if templates[0] not in template2mask_index:
                template2mask_index[templates[0]] = s1.index('[MASK]')
        else:
            template2sentences_out.setdefault(templates[1], []).append(s2)
            if templates[1] not in template2mask_index:
                template2mask_index[templates[1]] = s1.index('[MASK]')
    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]], mask_index: int):
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
