import random

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'even {nn1} ever {vbz} {det} {nn2} .',
    'g': 'only {nn1} ever {vbz} {det} {nn2} .',
}

template2 = {
    'b': 'even {nn1} {aux} ever {vb} {det} {nn2} .',
    'g': 'only {nn1} {aux} ever {vb} {det} {nn2} .',
}


def main():
    """
    example:
    "only sarah could ever talk." vs. "even sarah could ever talk"
    """

    vbzs = get_legal_words(tag='VBZ', exclude=('happens', 'says', ))
    vbs = get_legal_words(tag='VB')

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    determiners = ['the', 'this', 'some', 'that'] + ['your', 'his', 'her']

    auxiliaries = ['could', 'can', 'would', 'will']

    def add_argument_after_vb(v: str,
                              argument1: str,
                              ) -> str:
        if v in {'thinks', 'reads'}:
            return f'{v} about'
        elif v in {'lives', 'falls', 'is', 'be'}:
            return f'{v} in'
        elif v in {'stands', 'turns'}:
            return f'{v} on'
        elif v in {'acts', 'looks'}:
            return f'{v} like'
        elif v in {'goes', 'comes'}:
            return f'{v} to'
        elif v in {'gives', 'gives'}:
            return f'{v} {argument1}'
        elif v in {'plays', 'play', 'shows', 'show', 'tells', 'tell'}:
            return f'{v} {argument1}'
        else:
            return v

    while True:

        arg1 = random.choice(['him', 'her'])
        vbz = random.choice(vbzs)
        vb = random.choice(vbs)

        # random choices
        slot2filler = {
            'nn1': random.choice(names + animates),
            'nn2': random.choice(nouns_s),
            'vbz': add_argument_after_vb(vbz, arg1),
            'vb': add_argument_after_vb(vb, arg1),
            'det': random.choice(determiners),
            'aux': random.choice(auxiliaries)
        }

        # add determiner to animate noun
        if slot2filler['nn1'] in animates:
            slot2filler['nn1'] = random.choice(determiners) + ' ' + slot2filler['nn1']

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
