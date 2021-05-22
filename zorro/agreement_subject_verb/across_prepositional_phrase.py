import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'the {} on the {} {} {} .'
template2 = 'the {} by the {} {} {} .'

plural = inflect.engine()


def main():
    """
    example:
    "the dog on the mats is brown" vs "the dog on the mats are brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of sentences containing plural vs. singular object nouns
    2. subject with object number is counterbalanced such that:
        -singular subjects occur with 50:50 singular:plural objects
        -plural   subjects occur with 50:50 singular:plural objects
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN')
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ')

    copulas_singular = ["is", "was"]
    copulas_plural = ["are", "were"]

    while True:

        # counter-balance singular vs plural with subj vs. obj
        sub_s, sub_p = random.choice(nouns_s_and_p)
        obj_s, obj_p = random.choice(nouns_s_and_p)

        # random choices
        template = random.choice([template1, template2])
        adj = random.choice(adjectives)

        for copula_s in copulas_singular:
            # contrast is in number agreement between subject and copula
            yield template.format(sub_p, obj_s, copula_s, adj)  # bad
            yield template.format(sub_s, obj_s, copula_s, adj)  # good

            # same as above, except that object number is opposite
            yield template.format(sub_p, obj_p, copula_s, adj)
            yield template.format(sub_s, obj_p, copula_s, adj)

        for copula_p in copulas_plural:
            # contrast is in number agreement between subject and copula
            yield template.format(sub_s, obj_s, copula_p, adj)  # bad
            yield template.format(sub_p, obj_s, copula_p, adj)  # good

            # same as above, except that object number is opposite
            yield template.format(sub_s, obj_p, copula_p, adj)
            yield template.format(sub_p, obj_p, copula_p, adj)


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
