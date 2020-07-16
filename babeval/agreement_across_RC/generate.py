import random
from pathlib import Path

from babeval.vocab import get_vocab

NUM_NOUNS_FROM_EACH_LIST = 50  # there are 414 plurals
NUM_ADJECTIVES = 10

# object-relative clause
template1a = 'the {} that {} like [MASK] {} .'
template1b = 'the {} that {} likes [MASK] {} .'
# subject-relative clause - contains hint about number in relative clause
template2a = 'the {} that is there [MASK] {} .'
template2b = 'the {} that are there [MASK] {} .'

nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split()
nouns_plural = [w for w in nouns_plural if w in get_vocab()]

nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split()
nouns_singular = [w for w in nouns_singular if w in get_vocab()]

adjectives = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator2.txt').open().read().split()
adjectives = [w for w in adjectives if w in get_vocab()]

pronouns_1p_2p = ['I', 'you', 'we']
pronouns_1p_2p = [w for w in pronouns_1p_2p if w in get_vocab()]

pronouns_3p = ['he', 'she', 'it']
pronouns_3p = [w for w in pronouns_3p if w in get_vocab()]

assert len(pronouns_3p) == len(pronouns_1p_2p)


def main():

    random.seed(3)

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