import random

from zorro.agreement_across_RC import *

NUM_NOUNS_FROM_EACH_LIST = 50  # there are 414 plurals
NUM_ADJECTIVES = 10

# object-relative clause
template1a = 'the {} that {} like' + f' {configs.Data.mask_symbol} ' + '{} .'
template1b = 'the {} that {} likes' + f' {configs.Data.mask_symbol} ' + '{} .'
# subject-relative clause - contains hint about number in relative clause
template2a = 'the {} that is there' + f' {configs.Data.mask_symbol} ' + '{} .'
template2b = 'the {} that are there' + f' {configs.Data.mask_symbol} ' + '{} .'


def main():
    """
    example:
    "the dog that I like [MASK] lazy"
    """

    random.seed(configs.Data.seed)

    nouns_sample_singular = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST)
    nouns_sample_plural = random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)
    nouns_balanced = nouns_sample_singular + nouns_sample_plural

    adjectives_sample = random.sample(adjectives, k=NUM_ADJECTIVES)

    # object-relative

    for noun in nouns_balanced:
        for pronoun in pronouns_1p_2p:
            for adjective in adjectives_sample:
                yield template1a.format(noun, pronoun, adjective)

    for noun in nouns_balanced:
        for pronoun in pronouns_3p:
            for adjective in adjectives_sample:
                yield template1b.format(noun, pronoun, adjective)

    # subject-relative

    for noun in nouns_sample_singular:
        for adjective in adjectives_sample:
            yield template2a.format(noun, adjective)

    for noun in nouns_sample_plural:
        for adjective in adjectives_sample:
            yield template2b.format(noun, adjective)