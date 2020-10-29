import random

from babeval import configs


template1 = 'look at {} {} [MASK] .'
template2 = '{} {} [MASK] went there .'


def main():
    """
    example:
    "look at this green [MASK] .
    "these green [MASK] went there .
    """

    from babeval.agreement_across_1_adjective import adjectives, pre_nominals

    random.seed(configs.Data.seed)

    adjectives_sample = random.sample(adjectives, k=len(adjectives))

    for pre_nominal in pre_nominals:

        for adj in adjectives_sample:
            yield template1.format(pre_nominal, ' '.join([adj]))

            yield template2.format(pre_nominal, ' '.join([adj]))