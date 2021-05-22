import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset

template1 = '{} {} {} {} {} {} {} {} .'

plural = inflect.engine()


def main():
    """
    example:
    "a documentary was there looking at dogs ." vs. "there was a documentary looking at dogs ."
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN')
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ')

    quantifiers = ['each', 'most', 'all', 'every']

    copula_p = ['were', 'are', "were not", "aren't"]
    copula_s = ['was', 'is', "was not", "isn't"]

    vowels = {'a', 'e', 'i', 'o', 'u'}

    gerunds_ = [
        'looking',
        'becoming',
        'falling',
        'leaving',
        'eating',
        'increasing',
        'moving',
        'opening',
        'existing',
        'containing',
        'standing',
        'changing',
        'surrounding',
        'adding',
        'acting',
    ]
    gerunds = find_counterbalanced_subset(gerunds_, min_size=8, max_size=len(gerunds_))

    # a linker can be a preposition or determiner phrase
    gerund2linker = {
        'looking': 'like a',
        'becoming': 'some kind of a',
        'falling': 'on the',
        'leaving': 'us by the',
        'eating': 'one piece of this',
        'increasing': 'the size of the',
        'moving': 'to the',
        'opening': 'the door to a',
        'existing': 'without a',
        'containing': 'a',
        'standing': 'on top of a',
        'changing': 'the',
        'surrounding': 'the',
        'adding': 'to the',
        'acting': 'like a',
    }

    while True:

        # random choices
        noun_s, noun_p = random.choice(nouns_s_and_p)
        adj = random.choice(adjectives)
        quantifier = random.choice(quantifiers)
        subj_s, sub_p = random.choice(nouns_s_and_p)
        gerund = random.choice(gerunds)

        # plural vs. singular copula
        if quantifier in {'most', 'all'}:
            copula = random.choice(copula_p)
            subj1 = sub_p   # for template 1
        else:
            copula = random.choice(copula_s)
            subj1 = subj_s

        # "a" vs. "an"
        linker = gerund2linker[gerund]
        if linker.endswith('a') and adj[0] in vowels:
            linker += 'n'

        # contrast is about word order
        yield template1.format('there', copula, quantifier, subj1, gerund, linker, adj, noun_s)  # bad
        yield template1.format(quantifier, subj1, copula, 'there', gerund, linker, adj, noun_s)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
