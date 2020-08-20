import random

from babeval.agreement_across_1_adjective import *

template1 = 'look at {} {} [MASK] .'
template2 = '{} {} [MASK] went there .'


def main():
    """
    example:
    "look at this green [MASK] .
    "these green [MASK] went there .
    """

    random.seed(configs.Data.seed)

    adjectives_sample = random.sample(adjectives, k=len(adjectives))

    for pre_nominal in pre_nominals:

        for adj in adjectives_sample:
            yield template1.format(pre_nominal, ' '.join([adj]))

            yield template2.format(pre_nominal, ' '.join([adj]))