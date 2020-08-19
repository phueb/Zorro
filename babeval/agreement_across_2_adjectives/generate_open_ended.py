import random

from babeval.agreement_across_2_adjectives import *

template1 = 'look at {} {} [MASK] .'
template2 = '{} {} [MASK] went there .'


def main():
    """
    example:
    "look at this green [MASK] .
    "these green [MASK] went there .
    """

    random.seed(3)

    for pre_nominal in pre_nominals:

        al1 = random.sample(adjectives, k=len(adjectives))
        al2 = random.sample(adjectives, k=len(adjectives))

        for adj1, adj2 in zip(al1, al2):
            yield template1.format(pre_nominal, ' '.join([adj1]))
            yield template1.format(pre_nominal, ' '.join([adj1, adj2]))

            yield template2.format(pre_nominal, ' '.join([adj1]))
            yield template2.format(pre_nominal, ' '.join([adj1, adj2]))