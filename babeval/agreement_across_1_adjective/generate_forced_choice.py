import random

from babeval.agreement_across_1_adjective import *

NUM_ADJECTIVES = 10

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    "this green house went there ." vs. "this green houses went there."
    """

    random.seed(configs.Data.seed)

    adjectives_sample = random.sample(adjectives, k=NUM_ADJECTIVES)  # TODO re-generate sentences with this line outside outer loop

    for pre_nominal in pre_nominals:

        for adj in adjectives_sample:

            for noun_singular in nouns_singular:
                noun_plural = f'{noun_singular}s'  # TODO also handle irregular plurals
                if noun_plural not in nouns_plural:
                    continue

                yield template1.format(pre_nominal, ' '.join([adj]), noun_singular)
                yield template1.format(pre_nominal, ' '.join([adj]), noun_plural)

                yield template2.format(pre_nominal, ' '.join([adj]), noun_singular)
                yield template2.format(pre_nominal, ' '.join([adj]), noun_plural)
