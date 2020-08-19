from typing import List, Dict

from babeval.agreement_across_2_adjectives import *

SCORE_PLURAL_WORDPIECE_AS_CORRECT_PREDICTION = 1  # e.g. #bear", "##s"
SCORE_NOUN_WORDPIECE_AS_CORRECT_PREDICTION = 1  # e.g. "smooth", "##ie"


prediction_categories = (
    "noun +\ncorrect number",
    "noun +\nfalse number",
    "noun +\n ambiguous number",
    "noun\nproper",
    "non-start\nword-piece\nor\n[UNK]",
    "non-noun",
)


# score correct when start word is plural and predicted ##s turns adjective into a plural noun
if SCORE_PLURAL_WORDPIECE_AS_CORRECT_PREDICTION:
    nouns_plural.add('##s')


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}

    for s1, s2 in zip(sentences_in, sentences_out):
        if s1[0] == 'look':
            template2sentences_out.setdefault(templates[0], []).append(s2)
            if templates[0] not in template2mask_index:
                template2mask_index[templates[0]] = s1.index('[MASK]')
        elif s1[-2] == 'there':
            template2sentences_out.setdefault(templates[1], []).append(s2)
            if templates[1] not in template2mask_index:
                template2mask_index[templates[1]] = s1.index('[MASK]')
        else:
            raise ValueError(f'Failed to categorize template')

    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]],
                           mask_index: int) -> Dict[str, float]:

    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        pre_nominal = [w for w in sentence if w in pre_nominals][0]

        # non-start wordpiece
        if predicted_word.startswith("##") or predicted_word == '[UNK]':
            if predicted_word != '##s':
                res["non-start\nword-piece\nor\n[UNK]"] += 1
            elif not SCORE_PLURAL_WORDPIECE_AS_CORRECT_PREDICTION:
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
            res["noun +\n ambiguous number"] += 1

        # Non_Noun
        else:
            res["non-noun"] += 1

    return res
