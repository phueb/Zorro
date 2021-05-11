from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_agreement_between_two_words
from zorro.agreement_across_PP.shared import templates, copulas_plural, copulas_singular
from zorro.agreement_across_PP.shared import nouns_singular, nouns_plural


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        # template 1
        if s1[2] == 'on' and s2[2] == 'on':
            template2pairs.setdefault(templates[0], []).append(pair)
        # template 2
        elif s1[2] == 'by' and s2[2] == 'by':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          nouns_singular,
                          nouns_plural,
                          copulas_singular,
                          copulas_plural,
                          )
