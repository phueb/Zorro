from pathlib import Path
import random

from babeval.vocab import get_vocab


NUM_NOUNS_FROM_EACH_LIST = 50  # there are 414 plurals
NUM_ADJECTIVES = 20

template = 'look at [MASK] {} {} .'

adjectives = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator1.txt').open().read().split()
adjectives = [w for w in adjectives if w in get_vocab()]

nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split()
nouns_plural = [w for w in nouns_plural if w in get_vocab()]

nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split()
nouns_singular = [w for w in nouns_singular if w in get_vocab()]


def main():
    """
    use adjectives specifically selected for this task
    """

    random.seed(3)

    nouns_sample_singular = random.sample(nouns_singular, k=NUM_NOUNS_FROM_EACH_LIST)
    nouns_sample_plural = random.sample(nouns_plural, k=NUM_NOUNS_FROM_EACH_LIST)
    nouns_balanced = nouns_sample_singular + nouns_sample_plural

    for noun in nouns_balanced:

        # randomly sample adjectives from adjectives_list

        al1 = random.sample(adjectives, k=NUM_ADJECTIVES)
        al2 = random.sample(adjectives, k=NUM_ADJECTIVES)
        al3 = random.sample(adjectives, k=NUM_ADJECTIVES)

        for adj1, adj2, adj3 in zip(al1, al2, al3):
            yield template.format(' '.join([adj1]), noun)
            yield template.format(' '.join([adj1, adj2]), noun)
            yield template.format(' '.join([adj1, adj2, adj3]), noun)


