import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'where {} the {} go ?'
template2 = 'what {} the {} do ?'
template3 = 'how {} the {} fit in here ?'
template4 = 'how {} the {} become {} ?'
template5 = 'when {} the {} stop working ?'
template6 = 'when {} the {} start ?'

plural = inflect.engine()


def main():
    """
    example:
    "where does the dog go?" vs. "where does the dogs go?"
    """

    nouns_s_and_p = get_legal_words(tag='NN', second_tag='NNP')
    adjectives = get_legal_words(tag='JJ')

    doing_singular = ["does"]
    doing_plural = ["do"]

    while True:

        # random choices
        adj = random.choice(adjectives)
        noun_s, noun_p = random.choice(nouns_s_and_p)

        for doing_s in doing_singular:

            yield template1.format(doing_s, noun_p)  # bad
            yield template1.format(doing_s, noun_s)  # good

            yield template2.format(doing_s, noun_p)
            yield template2.format(doing_s, noun_s)

            yield template3.format(doing_s, noun_p)
            yield template3.format(doing_s, noun_s)

            yield template4.format(doing_s, noun_p, adj)
            yield template4.format(doing_s, noun_s, adj)

            yield template5.format(doing_s, noun_p)
            yield template5.format(doing_s, noun_s)

            yield template6.format(doing_s, noun_p)
            yield template6.format(doing_s, noun_s)

        for doing_p in doing_plural:
            yield template1.format(doing_p, noun_s)  # bad
            yield template1.format(doing_p, noun_p)   # good

            yield template2.format(doing_p, noun_s)
            yield template2.format(doing_p, noun_p)

            yield template3.format(doing_p, noun_s)
            yield template3.format(doing_p, noun_p)

            yield template4.format(doing_p, noun_s, adj)
            yield template4.format(doing_p, noun_p, adj)

            yield template5.format(doing_p, noun_s)
            yield template5.format(doing_p, noun_p)

            yield template6.format(doing_p, noun_s)
            yield template6.format(doing_p, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
