from typing import Union
import random

from zorro.data import DataExperimental, DataBaseline


def count_correct_choices(data: Union[DataExperimental, DataBaseline],
                          verbose: bool = False,
                          ) -> int:
    """
    for each sentence pair in the original, ordered file of test sentences,
     1) the cross entropy assigned to each by a model is retrieved
     2) some syntactic phenomenon (e.g. agreement = True or agreement = False) is evaluated
    When the cross-entropy assigned to the correct choice is higher,
     a value representing "correct" is incremented by one.

    """
    num_correct = 0  # num correct

    assert len(data.pairs) == len(data.grammatical_scores)

    # loop over all possible sentence pairs with all possible templates
    num_skipped = 0
    num_false = 0
    for (s1, s2), (is_grammatical1, is_grammatical2) in zip(data.pairs, data.grammatical_scores):

        # get cross-entropies
        xe1 = data.s2cross_entropies[tuple(s1)]
        xe2 = data.s2cross_entropies[tuple(s2)]

        # jitter cross-entropies when they are exactly identical
        if xe1 == xe2:
            if random.random() < 0.5:
                xe1 += 1
            else:
                xe2 += 1

        is_correct1 = is_grammatical1 and xe1 < xe2
        is_correct2 = is_grammatical2 and xe1 > xe2
        if is_correct1 or is_correct2:  # two ways to be correct
            num_correct += 1
        else:
            num_false += 1

    num_scored = num_correct + num_false
    num_expected_scores = len(data.pairs)

    if num_scored != num_expected_scores:
        print(f'Scored {num_correct} correct and {num_false} false and skipped {num_skipped}')
        raise RuntimeError(f'Expected {num_expected_scores:,} but got {num_scored:,} scores')

    if verbose:
        print(f'correct={num_correct:>9,}')
        print(f'false  ={num_false:>9,}')
        print(f'total  ={num_scored :>9,}')
        print(f'skipped={num_skipped :>9,}')
        print()

    return num_correct
