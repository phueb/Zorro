import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

# todo put templates in list, and loop over them, making sure each can be formatted in teh same way

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'
template3 = '{} {} {} did not happen .'
template4 = 'i saw {} {} {} .'

plural = inflect.engine()

paradigm = 'across_1_adjective'


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    "this green house went there ." vs. "this green houses went there."
    """

    demonstratives_singular = ["this", "that"]
    demonstratives_plural = ["these", "those"]

    nouns_s_and_p = get_legal_words(tag='NN', second_tag='NNP')
    adjectives = get_legal_words(tag='JJ')

    while True:

        # random choices
        adj = random.choice(adjectives)
        noun_s, noun_p = random.choice(nouns_s_and_p)

        for dem_s in demonstratives_singular:
            yield template1.format(dem_s, adj, noun_p)  # odd numbered line: bad
            yield template1.format(dem_s, adj, noun_s)  # even numbered line: good

            yield template2.format(dem_s, adj, noun_p)
            yield template2.format(dem_s, adj, noun_s)

            yield template3.format(dem_s, adj, noun_p)
            yield template3.format(dem_s, adj, noun_s)

            yield template4.format(dem_s, adj, noun_p)
            yield template4.format(dem_s, adj, noun_s)

        for dem_p in demonstratives_plural:
            yield template1.format(dem_p, adj, noun_s)  # odd numbered line: bad
            yield template1.format(dem_p, adj, noun_p)  # even numbered line: good

            yield template2.format(dem_p, adj, noun_s)
            yield template2.format(dem_p, adj, noun_p)

            yield template3.format(dem_p, adj, noun_s)
            yield template3.format(dem_p, adj, noun_p)

            yield template4.format(dem_p, adj, noun_s)
            yield template4.format(dem_p, adj, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
