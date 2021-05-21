import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'where {} the {} ?'
template2 = 'what {} the {} ?'
template3 = 'what color {} the {} ?'
template4 = '{} the {} not {} ?'
template5 = '{} the {} where it should be ?'
template6 = '{} the {} where they should be ?'
template7 = '{} the {} something you like ?'
template8 = '{} the {} a good idea ?'

plural = inflect.engine()


def main():
    """
    example:
    "where is the house?" vs "where is the houses?"
    todo "where is the house?" vs "where are the house?"
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    copulas_singular = ["is", "was"]
    copulas_plural = ["are", "were"]

    while True:

        # random choices
        noun_s, noun_p = random.choice(nouns_s_and_p)
        adj = random.choice(adjectives)

        for copula_s in copulas_singular:

            yield template1.format(copula_s, noun_p)
            yield template1.format(copula_s, noun_s)

            yield template2.format(copula_s, noun_p)
            yield template2.format(copula_s, noun_s)

            yield template3.format(copula_s, noun_p)
            yield template3.format(copula_s, noun_s)

            yield template4.format(copula_s, noun_p, adj)
            yield template4.format(copula_s, noun_s, adj)

            yield template5.format(copula_s, noun_p)
            yield template5.format(copula_s, noun_s)

            # skip template 6 because it is specific to plural copula

            yield template7.format(copula_s, noun_p)
            yield template7.format(copula_s, noun_s)

            yield template8.format(copula_s, noun_p)
            yield template8.format(copula_s, noun_s)

        for copula_p in copulas_plural:

            yield template1.format(copula_p, noun_s)
            yield template1.format(copula_p, noun_p)

            yield template2.format(copula_p, noun_s)
            yield template2.format(copula_p, noun_p)

            yield template3.format(copula_p, noun_s)
            yield template3.format(copula_p, noun_p)

            yield template4.format(copula_p, noun_s, adj)
            yield template4.format(copula_p, noun_p, adj)

            # skip template 5 because it is specific to singular copula

            yield template6.format(copula_p, noun_s)
            yield template6.format(copula_p, noun_p)

            yield template7.format(copula_p, noun_s)
            yield template7.format(copula_p, noun_p)

            yield template8.format(copula_p, noun_s)
            yield template8.format(copula_p, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
