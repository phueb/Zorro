import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

template1a = 'the {} that {} like {} {} .'
template1b = 'the {} that {} likes {} {} .'
template2a = 'the {} that was there {} {} .'
template2b = 'the {} that were there {} {} .'

plural = inflect.engine()


def main():
    """
    example:
    "the dog that i like is green" vs. "the dogs that i like is green"
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN')
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ')

    copulas_singular = ["is", "was"]
    copulas_plural = ["are", "were"]

    pronouns_1p_2p = ['i', 'you', 'we']
    pronouns_3p = ['he', 'she', 'it']
    assert len(pronouns_3p) == len(pronouns_1p_2p)

    while True:

        # random choices
        noun_s, noun_p = random.choice(nouns_s_and_p)
        adj = random.choice(adjectives)

        for copula_s in copulas_singular:

            # object-relative
            for pronoun_1p_2p in pronouns_1p_2p:
                yield template1a.format(noun_p, pronoun_1p_2p, copula_s, adj)  # bad
                yield template1a.format(noun_s, pronoun_1p_2p, copula_s, adj)  # good
            for pronoun_3p in pronouns_3p:
                yield template1b.format(noun_p, pronoun_3p, copula_s, adj)
                yield template1b.format(noun_s, pronoun_3p, copula_s, adj)

            # subject-relative
            yield template2a.format(noun_p, copula_s, adj)
            yield template2a.format(noun_s, copula_s, adj)

            for copula_p in copulas_plural:

                # object-relative
                for pronoun_1p_2p in pronouns_1p_2p:
                    yield template1a.format(noun_s, pronoun_1p_2p, copula_p, adj)
                    yield template1a.format(noun_p, pronoun_1p_2p, copula_p, adj)
                for pronoun_3p in pronouns_3p:
                    yield template1b.format(noun_s, pronoun_3p, copula_p, adj)
                    yield template1b.format(noun_p, pronoun_3p, copula_p, adj)

                # subject-relative
                yield template2b.format(noun_s, copula_p, adj)
                yield template2b.format(noun_p, copula_p, adj)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
