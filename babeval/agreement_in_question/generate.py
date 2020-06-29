import random
from pathlib import Path

from babeval.vocab import get_vocab

NUM_NOUNS_FROM_EACH_LIST = 400  # there are only 414 plurals

template1 = 'where [MASK] the {} ?'
template2 = 'where [MASK] the {} go ?'
template4 = 'what [MASK] the {} ?'
template3 = 'what [MASK] the {} do ?'

nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split()
nouns_plural = [w for w in nouns_plural if w in get_vocab()]

nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split()
nouns_singular = [w for w in nouns_singular if w in get_vocab()]


def main():
    random.seed(2)

    nouns_balanced = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST) + \
                     random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)

    for noun in nouns_balanced:
        yield template1.format(noun)
        yield template2.format(noun)
        yield template3.format(noun)
        yield template4.format(noun)
