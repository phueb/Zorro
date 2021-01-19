from typing import List, Dict, Tuple
from functools import partial

from zorro.agreement_across_2_adjectives.shared import templates, pre_nominals_plural, pre_nominals_singular
from zorro.agreement_across_2_adjectives.shared import nouns_singular, nouns_plural
from zorro.grammatical import check_agreement_between_two_words

prediction_categories = ('correct', )


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[0] == 'look' and s2[0] == 'look':
            template2pairs.setdefault(templates[0], []).append(pair)
        elif s1[-2] == 'there' and s2[-2] == 'there':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize "{pair}" to template.')

    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          pre_nominals_singular,
                          pre_nominals_plural,
                          nouns_singular,
                          nouns_plural,
                          )
