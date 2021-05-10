from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_irregular_past_participle
from zorro.irregular_past_participle_verb_intransitive.shared import templates


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[0] == 'the' and s2[3] == 'the':
            template2pairs.setdefault(templates[0], []).append(pair)

        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


grammar_checker = partial(check_irregular_past_participle,

                          )
