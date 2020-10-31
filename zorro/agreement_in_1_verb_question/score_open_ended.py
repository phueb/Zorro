from typing import List, Dict

from zorro.agreement_in_1_verb_question import *


prediction_categories = (
    'non-start\nsub-token\nor\n[UNK]',
    "copula\ncorrect",
    "copula\nfalse",
    "other",
)


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}

    for s1, s2 in zip(sentences_in, sentences_out):
        template2sentences_out.setdefault(templates[0], []).append(s2)
        if templates[0] not in template2mask_index:
            template2mask_index[templates[0]] = s1.index(configs.Data.mask_symbol)
    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]],
                           mask_index: int) -> Dict[str, float]:

    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        targeted_noun = sentence[3]

        if not predicted_word.startswith(configs.Data.space_symbol) or predicted_word == "[UNK]":
            res['non-start\nsub-token\nor\n[UNK]'] += 1

        elif targeted_noun in nouns_plural and predicted_word in subjective_copula_plural:
            res["copula\ncorrect"] += 1
        elif targeted_noun in nouns_singular and predicted_word in subjective_copula_singular:
            res["copula\ncorrect"] += 1

        elif targeted_noun in nouns_plural and predicted_word in subjective_copula_singular:
            res["copula\nfalse"] += 1
        elif targeted_noun in nouns_singular and predicted_word in subjective_copula_plural:
            res["copula\nfalse"] += 1

        else:
            res["other"] += 1

    return res
