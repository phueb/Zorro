import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': '{name1} {vbd} one {nn} and {name2} {vbd} {number} {jj} .',
    'g': '{name1} {vbd} one {jj} {nn} and {name2} {vbd} {number} .',
}

template2 = {
    'b': '{det} {nn2} {vbd} one {nn} and {name2} {vbd} {number} {jj} .',
    'g': '{det} {nn2} {vbd} one {jj} {nn} and {name2} {vbd} {number} .',
}


plural = inflect.engine()


def main():
    """
    example:
    "sam found one purple dog and karen revealed more ." vs. "sam found one dog and karen revealed more purple."
    """

    vbds = get_legal_words(tag='VBD')
    adjectives = get_legal_words(tag='JJ')

    nouns_mass = (configs.Dirs.legal_words / 'nouns_mass.txt').open().read().split()
    nouns_s = get_legal_words(tag='NN', exclude=tuple(nouns_mass))

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    determiners = ['a', 'the', 'this', 'some', 'that'] + ['your', 'his', 'her']

    number_words = ['several', 'more', 'two', 'three', 'a lot more']  # , 'some']

    while True:

        # random choices
        slot2filler = {
            'name1': random.choice(names),
            'name2': random.choice(names),
            'nn': random.choice(nouns_s),
            'nn2': random.choice(animates),
            'vbd': random.choice(vbds),
            'det': random.choice(determiners),
            'jj': random.choice(adjectives),
            'number': random.choice(number_words),
        }

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
