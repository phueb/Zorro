from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_irregular_verb_passive
from zorro.irregular_verb_passive.shared import templates, vds_vns


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


verbs_correct = [vn for vd, vn in vds_vns]
grammar_checker = partial(check_irregular_verb_passive,
                          verbs_correct,
                          )
