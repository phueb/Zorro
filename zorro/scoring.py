from typing import List, Tuple, Dict, Callable


def count_correct_choices(pairs: List[Tuple[List[str], List[str]]],
                          grammatical_scores: List[Tuple[bool, bool]],
                          s2cross_entropies: Dict[Tuple[str], float],
                          ) -> int:
    """
    for each sentence pair in the original, ordered file of test sentences,
     1) the cross entropy assigned to each by a model is retrieved
     2) some syntactic phenomenon (e.g. agreement = True or agreement = False) is evaluated
    When the cross-entropy assigned to the correct choice is higher,
     a value representing "correct" is incremented by one.

    """
    res = 0  # num correct

    # loop over all possible sentence pairs with all possible templates
    num_skipped = 0
    num_false = 0
    for (s1, s2), (is_grammatical1, is_grammatical2) in zip(pairs, grammatical_scores):

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

        is_correct1 = is_grammatical1 and xe1 < xe2
        is_correct2 = is_grammatical2 and xe1 > xe2
        if is_correct1 or is_correct2:  # two ways to be correct
            res += 1
        else:
            num_false += 1

    num_scored = res + num_false
    num_expected_scores = len(pairs)

    if num_scored != num_expected_scores:
        print(f'Scored {res} correct and {num_false} false and skipped {num_skipped}')
        raise RuntimeError(f'Expected {num_expected_scores:,} but got {num_scored:,} scores')

    print(f'correct={res:>9,}')
    print(f'false  ={num_false:>9,}')
    print(f'total  ={num_scored :>9,}')
    print(f'skipped={num_skipped :>9,}')
    print()

    return res


def check_pairs_for_grammar(pairs: List[Tuple[List[str], List[str]]],
                            grammar_checker: Callable,
                            ) -> List[Tuple[bool, bool]]:

    res = []

    for s1, s2 in pairs:

        is_grammatical1 = grammar_checker(s1)
        is_grammatical2 = grammar_checker(s2)

        if len({is_grammatical1, is_grammatical2}) == 1:  # are both False or both True?
            print(s1, is_grammatical1)
            print(s2, is_grammatical2)
            res.append((True, False))
            # raise ValueError('Only one sentence per pair can be correct/agree in number.')  #TODO reinstate
            print('Only one sentence per pair can be correct/agree in number.')  #TODO reinstate
        else:
            res.append((is_grammatical1, is_grammatical2))

    return res
