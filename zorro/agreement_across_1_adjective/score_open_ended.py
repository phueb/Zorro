from typing import List, Dict

from zorro import configs
from zorro.agreement_across_1_adjective.shared import templates, pre_nominals_plural, pre_nominals_singular
from zorro.agreement_across_1_adjective.shared import nouns_singular, nouns_plural


prediction_categories = (
    "noun +\ncorrect number",
    "noun +\nfalse number",
    "noun +\n no number",
    "noun\nproper",
    's',
    "non-noun",
)

# external
nouns_ambiguous = (configs.Dirs.external_words / 'nouns_ambiguous_number.txt').open().read().split("\n")
nouns_proper = (configs.Dirs.external_words / 'nouns_proper.txt').open().read().split("\n")


def categorize_by_template(sentences_in, productions: List[List[str]]):

    template2productions = {}
    template2mask_index = {}

    for s1, s2 in zip(sentences_in, productions):
        if s1[0] == 'look':
            template2productions.setdefault(templates[0], []).append(s2)
            if templates[0] not in template2mask_index:
                template2mask_index[templates[0]] = s1.index(configs.Data.mask_symbol)
        elif s1[-2] == 'there':
            template2productions.setdefault(templates[1], []).append(s2)
            if templates[1] not in template2mask_index:
                template2mask_index[templates[1]] = s1.index(configs.Data.mask_symbol)
        else:
            print(s1, s2)
            raise ValueError(f'Failed to categorize template')

    return template2productions, template2mask_index


def categorize_predictions(productions: List[List[str]],
                           mask_index: int) -> Dict[str, float]:

    res = {k: 0 for k in prediction_categories}

    for sentence in productions:
        predicted_word = sentence[mask_index]
        pre_nominal = [w for w in sentence if w in pre_nominals_singular + pre_nominals_plural][0]

        # non-start sub-word    # todo still relevant with bbpe?
        if predicted_word == 's':
            res['s'] += 1

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
