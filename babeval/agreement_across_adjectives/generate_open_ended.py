from pathlib import Path
import random

from babeval.vocab import get_vocab

template = 'look at {} {} [MASK] .'

pre_nominals = ['this', 'these', 'that', 'those']

adjectives = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator2.txt').open().read().split()
adjectives = [w for w in adjectives if w in get_vocab()]


def main():
    """
    example:
    "look at this green [MASK].
    """

    random.seed(3)

    for pre_nominal in pre_nominals:

        al1 = random.sample(adjectives, k=len(adjectives))
        al2 = random.sample(adjectives, k=len(adjectives))
        al3 = random.sample(adjectives, k=len(adjectives))

        for adj1, adj2, adj3 in zip(al1, al2, al3):
            yield template.format(pre_nominal, ' '.join([adj1]))
            yield template.format(pre_nominal, ' '.join([adj1, adj2]))
            yield template.format(pre_nominal, ' '.join([adj1, adj2, adj3]))