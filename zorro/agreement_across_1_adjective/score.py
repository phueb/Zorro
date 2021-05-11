from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_agreement_between_two_words
from zorro.agreement_across_1_adjective.shared import templates, pre_nominals_plural, pre_nominals_singular
from zorro.agreement_across_1_adjective.shared import nouns_singular, nouns_plural



def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        # template 1
        if s1[0] == 'look' and s2[0] == 'look':
            template2pairs.setdefault(templates[0], []).append(pair)
        # template 2
        elif s1[-2] == 'there' and s2[-2] == 'there':
            template2pairs.setdefault(templates[1], []).append(pair)
        # template 3
        elif s1[-2] == 'here' and s2[-2] == 'here':
            template2pairs.setdefault(templates[2], []).append(pair)
        # template 4
        elif s1[1] == 'saw' and s2[1] == 'saw':
            template2pairs.setdefault(templates[3], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          pre_nominals_singular,
                          pre_nominals_plural,
                          nouns_singular,
                          nouns_plural,
                          )
