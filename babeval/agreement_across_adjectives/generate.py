from pathlib import Path
import random

from babeval.vocab import get_vocab

template = 'look at {} {} [MASK] .'

pre_nominals = ['this', 'these', 'that', 'those']

adjectives_list = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator1.txt').open().read().split()
adjectives_list = [w for w in adjectives_list if w in get_vocab()]


def main():
    """
    example:
    "look at this green [MASK].
    """

    random.seed(3)

    for pre_nominal in pre_nominals:

        al1 = random.sample(adjectives_list, k=len(adjectives_list))
        al2 = random.sample(adjectives_list, k=len(adjectives_list))
        al3 = random.sample(adjectives_list, k=len(adjectives_list))

        for adj1, adj2, adj3 in zip(al1, al2, al3):
            yield template.format(pre_nominal, ' '.join([adj1]))
            yield template.format(pre_nominal, ' '.join([adj1, adj2]))
            yield template.format(pre_nominal, ' '.join([adj1, adj2, adj3]))