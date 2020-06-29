import random
from pathlib import Path

from babeval.vocab import get_vocab

NUM_NOUNS_FROM_EACH_LIST = 400  # there are only 414 plurals

template1 = 'the {} that {} like [MASK] {} .'
template2 = 'the {} that {} likes [MASK] {} .'

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

    random.seed(2)

    nouns_balanced = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST) + \
                     random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)

    for noun in nouns_balanced:
        for pronoun in pronouns_1p_2p:
            for adjective in adjectives:
                yield template1.format(noun, pronoun, adjective)

    for noun in nouns_balanced:
        for pronoun in pronouns_3p:
            for adjective in adjectives:
                yield template2.format(noun, pronoun, adjective)