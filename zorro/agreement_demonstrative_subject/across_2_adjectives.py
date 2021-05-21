import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

# todo put templates in list, and loop over them, making sure each can be formatted in teh same way

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'
template3 = '{} {} {} did not happen .'
template4 = 'i saw {} {} {} .'

plural = inflect.engine()


def main():
    """
    example:
    "look at this green red house ." vs. "look at this green red houses ."

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
        adj1_and2 = f'{random.choice(adjectives)} {random.choice(adjectives)}'
        noun_s, noun_p = random.choice(nouns_s_and_p)

        for dem_s in demonstratives_singular:
            yield template1.format(dem_s, adj1_and2, noun_p)  # odd numbered line: bad
            yield template1.format(dem_s, adj1_and2, noun_s)  # even numbered line: good

            yield template2.format(dem_s, adj1_and2, noun_p)
            yield template2.format(dem_s, adj1_and2, noun_s)

            yield template3.format(dem_s, adj1_and2, noun_p)
            yield template3.format(dem_s, adj1_and2, noun_s)

            yield template4.format(dem_s, adj1_and2, noun_p)
            yield template4.format(dem_s, adj1_and2, noun_s)

        for dem_p in demonstratives_plural:
            yield template1.format(dem_p, adj1_and2, noun_s)  # odd numbered line: bad
            yield template1.format(dem_p, adj1_and2, noun_p)  # even numbered line: good

            yield template2.format(dem_p, adj1_and2, noun_s)
            yield template2.format(dem_p, adj1_and2, noun_p)

            yield template3.format(dem_p, adj1_and2, noun_s)
            yield template3.format(dem_p, adj1_and2, noun_p)

            yield template4.format(dem_p, adj1_and2, noun_s)
            yield template4.format(dem_p, adj1_and2, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
