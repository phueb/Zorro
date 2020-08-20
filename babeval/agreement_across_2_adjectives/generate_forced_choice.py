import random

from babeval.agreement_across_2_adjectives import *

NUM_ADJECTIVES = 10

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'


def main():
    """
    example:
    "look at this green red house ." vs. "look at this green red houses ."
    "this green red house went there ." vs. "this green red houses went there."
    """

    random.seed(configs.Data.seed)

    for pre_nominal in pre_nominals:

        al1 = random.sample(adjectives, k=NUM_ADJECTIVES)
        al2 = random.sample(adjectives, k=NUM_ADJECTIVES)

        for adj1, adj2 in zip(al1, al2):

            for noun_singular in nouns_singular:
                noun_plural = f'{noun_singular}s'  # TODO also handle irregular plurals
                if noun_plural not in nouns_plural:
                    continue

                yield template1.format(pre_nominal, ' '.join([adj1, adj2]), noun_singular)
                yield template1.format(pre_nominal, ' '.join([adj1, adj2]), noun_plural)

                yield template2.format(pre_nominal, ' '.join([adj1, adj2]), noun_singular)
                yield template2.format(pre_nominal, ' '.join([adj1, adj2]), noun_plural)