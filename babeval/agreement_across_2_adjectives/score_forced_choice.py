from typing import List, Dict, Tuple

from babeval.agreement_across_2_adjectives.shared import templates, pre_nominals_plural, pre_nominals_singular
from babeval.utils import check_agreement_between_pre_nominal_and_noun

prediction_categories = ('false', 'correct')


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


def categorize_predictions(pairs: List[Tuple[List[str], List[str]]],
                           s2cross_entropies: Dict[Tuple[str], float]) -> Dict[str, float]:
    """
    for each sentence pair in the original, ordered file of test sentences,
     1) the cross entropy assigned to each by a to-be-evaluated model is retrieved
     2) some syntactic phenomenon (e.g. agreement = True or agreement = False) is evaluated
    When the cross-entropy assigned to the correct choice is higher,
     a value representing "correct" is incremented by one.

    """
    res = {k: 0 for k in prediction_categories}

    # loop over all possible sentence pairs with all possible templates
    num_skipped = 0
    for s1, s2 in pairs:

        # check agreement
        is_agreement1 = check_agreement_between_pre_nominal_and_noun(s1,
                                                                     pre_nominals_singular,
                                                                     pre_nominals_plural,
                                                                     nouns_singular,
                                                                     nouns_plural,
                                                                     )
        is_agreement2 = check_agreement_between_pre_nominal_and_noun(s2,
                                                                     pre_nominals_singular,
                                                                     pre_nominals_plural,
                                                                     nouns_singular,
                                                                     nouns_plural,
                                                                     )
        if len({is_agreement1, is_agreement2}) != 2:  # check that only 1 but not both are True
            raise ValueError('Only one sentence per pair can be correct/agree in number.')

        # get cross-entropies
        try:
            xe1 = s2cross_entropies[tuple(s1)]
            xe2 = s2cross_entropies[tuple(s2)]
        except KeyError:  # happens when original test sentences are different than what model was tested with
            # try sentences without punctuation (if model was probed with sentences stripped of punctuation)
            try:
                xe1 = s2cross_entropies[tuple(s1[:-1])]
                xe2 = s2cross_entropies[tuple(s2[:-1])]
            except KeyError:
                num_skipped += 1
                continue

        is_correct1 = is_agreement1 and xe1 < xe2
        is_correct2 = is_agreement2 and xe1 > xe2
        if is_correct1 or is_correct2:  # two ways to be correct
            res["correct"] += 1
        else:
            res["false"] += 1

    num_scored = res["false"] + res["correct"]
    num_expected_scores = len(pairs)

    if num_scored != num_expected_scores:
        raise RuntimeError(f'Expected {num_expected_scores:,} but got {num_scored:,} scores')

    print(f'correct={res["correct"]:>9,}')
    print(f'false  ={res["false"]:>9,}')
    print(f'total  ={num_scored :>9,}')
    print(f'skipped={num_skipped :>9,}')
    print()

    return res
