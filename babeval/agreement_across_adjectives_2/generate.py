from pathlib import Path
import random

from babeval.vocab import get_vocab

"""
Look at [MASK] fighting toy .
[MASK] should be replaced with start_word
"""

template = 'look at [MASK] {} {} .'

adjectives_list = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator1.txt').open().read().split()
adjectives_list = [w for w in adjectives_list if w in get_vocab()]

nouns_list = (Path(__file__).parent / 'word_lists' / 'nouns_annotator2.txt').open().read().split()
nouns_list = [w for w in nouns_list if w in get_vocab()]


def main():
    """
    use adjectives specifically selected for this task
    """

    random.seed(3)

    for noun in nouns_list:

        # randomly sample adjectives from adjectives_list

        al1 = random.sample(adjectives_list, k=len(adjectives_list))
        al2 = random.sample(adjectives_list, k=len(adjectives_list))
        al3 = random.sample(adjectives_list, k=len(adjectives_list))

        for adj1, adj2, adj3 in zip(al1, al2, al3):
            yield template.format(' '.join([adj1]), noun)
            yield template.format(' '.join([adj1, adj2]), noun)
            yield template.format(' '.join([adj1, adj2, adj3]), noun)


