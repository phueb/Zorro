from typing import List, Dict

from babeval.agreement_across_PP import *

prediction_categories = (
    "non-start\nword-piece\nor\n[UNK]",
    "correct\ncopula",
    "false\ncopula",
    "other")


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}

    for s1, s2 in zip(sentences_in, sentences_out):
        template2sentences_out.setdefault(templates[0], []).append(s2)
        if templates[0] not in template2mask_index:
            template2mask_index[templates[0]] = s1.index('[MASK]')
    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]],
                           mask_index: int) -> Dict[str, float]:

    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]  # predicted word may not be a copula ("is", "are")
        targeted_noun = sentence[1]

        if predicted_word.startswith('##') or predicted_word == "[UNK]":
            res["non-start\nword-piece\nor\n[UNK]"] += 1

        elif targeted_noun in nouns_plural and predicted_word in copulas_plural:
            res["correct\ncopula"] += 1

        elif targeted_noun in nouns_singular and predicted_word in copulas_singular:
            res["correct\ncopula"] += 1

        elif targeted_noun in nouns_plural and predicted_word in copulas_singular:
            res["false\ncopula"] += 1

        elif targeted_noun in nouns_singular and predicted_word in copulas_plural:
            res["false\ncopula"] += 1

        else:
            res['other'] += 1

    return res
