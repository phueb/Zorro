from typing import List, Dict

from zorro.agreement_across_RC.shared import templates, copulas_plural, copulas_singular
from zorro.agreement_across_RC.shared import nouns_singular, nouns_plural
from zorro import configs

prediction_categories = (
    's',
    "correct\ncopula",
    "false\ncopula",
    "other",
)


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        if s1[4] in {'like', 'likes'}:
            template2sentences_out.setdefault(templates[0], []).append(s2)
            if templates[0] not in template2mask_index:
                template2mask_index[templates[0]] = s1.index(configs.Data.mask_symbol)
        else:
            template2sentences_out.setdefault(templates[1], []).append(s2)
            if templates[1] not in template2mask_index:
                template2mask_index[templates[1]] = s1.index(configs.Data.mask_symbol)
    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]],
                           mask_index: int) -> Dict[str, float]:

    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        targeted_noun = sentence[1]

        if predicted_word == 's':
            res['s'] += 1

        elif targeted_noun in nouns_plural and predicted_word in copulas_plural:
            res["correct\ncopula"] += 1
        elif targeted_noun in nouns_singular and predicted_word in copulas_singular:
            res["correct\ncopula"] += 1

        elif targeted_noun in nouns_plural and predicted_word in copulas_singular:
            res["false\ncopula"] += 1
        elif targeted_noun in nouns_singular and predicted_word in copulas_plural:
            res["false\ncopula"] += 1

        else:
            res["other"] += 1

    return res

