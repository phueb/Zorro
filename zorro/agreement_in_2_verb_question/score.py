from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_agreement_between_two_words
from zorro.agreement_in_2_verb_question.shared import templates, doing_singular, doing_plural
from zorro.agreement_in_2_verb_question.shared import nouns_singular, nouns_plural


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[0] == 'where' and s2[0] == 'where':
            template2pairs.setdefault(templates[0], []).append(pair)
        elif s1[0] == 'what' and s2[0] == 'what':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          doing_singular,
                          doing_plural,
                          nouns_singular,
                          nouns_plural,
                          )

