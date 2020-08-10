from pathlib import Path
import random

from babeval.vocab import get_vocab

NUM_ADJECTIVES = 10
INCLUDE_THREE_ADJECTIVES_TEMPLATE = False

template = 'look at {} {} {} .'

pre_nominals = ['this', 'these', 'that', 'those']

adjectives = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator2.txt').open().read().split()
adjectives = [w for w in adjectives if w in get_vocab()]

nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split()
nouns_plural = [w for w in nouns_plural if w in get_vocab()]

nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split()
nouns_singular = [w for w in nouns_singular if w in get_vocab()]

nouns_plural_set = set(nouns_plural)


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    """

    random.seed(3)

    for pre_nominal in pre_nominals:

        al1 = random.sample(adjectives, k=NUM_ADJECTIVES)
        al2 = random.sample(adjectives, k=NUM_ADJECTIVES)
        al3 = random.sample(adjectives, k=NUM_ADJECTIVES)

        for adj1, adj2, adj3 in zip(al1, al2, al3):

            for noun_singular in nouns_singular:
                noun_plural = f'{noun_singular}s'  # TODO also handle irregular plurals
                if noun_plural not in nouns_plural_set:
                    continue

                yield template.format(pre_nominal, ' '.join([adj1]), noun_singular)
                yield template.format(pre_nominal, ' '.join([adj1]), noun_plural)

                yield template.format(pre_nominal, ' '.join([adj1, adj2]), noun_singular)
                yield template.format(pre_nominal, ' '.join([adj1, adj2]), noun_plural)

                if INCLUDE_THREE_ADJECTIVES_TEMPLATE:
                    yield template.format(pre_nominal, ' '.join([adj1, adj2, adj3]), noun_singular)
                    yield template.format(pre_nominal, ' '.join([adj1, adj2, adj3]), noun_plural)