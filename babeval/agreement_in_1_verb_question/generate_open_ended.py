import random

from babeval.agreement_in_1_verb_question import *

NUM_NOUNS_FROM_EACH_LIST = 400  # there are only 414 plurals

template1 = 'where [MASK] the {} ?'
template2 = 'what [MASK] the {} ?'


def main():
    random.seed(3)

    nouns_balanced = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST) + \
                     random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)

    for noun in nouns_balanced:
        yield template1.format(noun)
        yield template2.format(noun)

