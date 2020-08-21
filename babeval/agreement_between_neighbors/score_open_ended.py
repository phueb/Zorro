from typing import List, Dict

from babeval.agreement_between_neighbors import *

SCORE_PLURAL_WORDPIECE_AS_CORRECT_PREDICTION = 1


prediction_categories = (
    "noun +\ncorrect number",
    "noun +\nfalse number",
    "noun +\n no number",
    "noun\nproper",
    "non-start\nword-piece\nor\n[UNK]",
    "non-noun",
)


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
        predicted_word = sentence[mask_index]
        pre_nominal = [w for w in sentence if w in pre_nominals][0]

        # non-start wordpiece
        if predicted_word.startswith("##") or predicted_word == '[UNK]':
            res["non-start\nword-piece\nor\n[UNK]"] += 1

        # proper noun
        if predicted_word in nouns_proper:
            res["noun\nproper"] += 1

        # correct Noun Number
        elif predicted_word in nouns_plural and pre_nominal in pre_nominals_plural:
            res["noun +\ncorrect number"] += 1

        elif predicted_word in nouns_singular and pre_nominal in pre_nominals_singular:
            res["noun +\ncorrect number"] += 1

        # false Noun Number
        elif predicted_word in nouns_plural and pre_nominal in pre_nominals_singular:
            res["noun +\nfalse number"] += 1

        elif predicted_word in nouns_singular and pre_nominal in pre_nominals_plural:
            res["noun +\nfalse number"] += 1

        # Ambiguous Noun
        elif predicted_word in nouns_ambiguous:
            res["noun +\n no number"] += 1

        # Non_Noun
        else:
            res["non-noun"] += 1

    return res
