from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_irregular_past_participle_verb
from zorro.irregular_past_participle_verb_intransitive.shared import templates, vb2vbd_vbn_intransitive


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[-1] == '.':
            template2pairs.setdefault(templates[0], []).append(pair)

        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


verb_position = 3  # zero-index
grammar_checker = partial(check_irregular_past_participle_verb,
                          vb2vbd_vbn_intransitive,
                          verb_position,
                          )
