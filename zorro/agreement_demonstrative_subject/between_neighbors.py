import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = '{} {} must be {} .'
template2 = '{} {} can be {} .'

templates = []

plural = inflect.engine()


def main():
    """
    example:
    "look at this house" vs. "look at this houses"

    note: all odd numbered sentences are bad and even good.
    """

    demonstratives_singular = ["this", "that"]
    demonstratives_plural = ["these", "those"]

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    while True:

        # random choices
        noun_s, noun_p = random.choice(nouns_s_and_p)
        adj = random.choice(adjectives)

        for dem_s in demonstratives_singular:

            yield template1.format(dem_s, noun_p, adj)  # bad
            yield template1.format(dem_s, noun_s, adj)  # good

            yield template2.format(dem_s, noun_p, adj)
            yield template2.format(dem_s, noun_s, adj)

        for dem_p in demonstratives_plural:
            yield template1.format(dem_p, noun_s, adj)  # bad
            yield template1.format(dem_p, noun_p, adj)  # good

            yield template2.format(dem_p, noun_s, adj)
            yield template2.format(dem_p, noun_p, adj)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
