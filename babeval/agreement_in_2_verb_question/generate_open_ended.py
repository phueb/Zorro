import random
from pathlib import Path

from babeval import configs

NUM_NOUNS_FROM_EACH_LIST = 400  # there are only 414 plurals

template1 = 'where [MASK] the {} go ?'
template2 = 'what [MASK] the {} do ?'

nouns_plural = (Path(__file__).parent / configs.Data.annotator / 'nouns_plural.txt').open().read().split()
nouns_singular = (Path(__file__).parent / configs.Data.annotator / 'nouns_singular.txt').open().read().split()


def main():
    random.seed(3)

    nouns_balanced = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST) + \
                     random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)

    for noun in nouns_balanced:
        yield template1.format(noun)
        yield template2.format(noun)
