import random

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': '{name} {vbd} what the {nn1} could {vb} the {nn2} .',
    'g': '{name} {vbd} the {nn1} that the {nn2} could {vb} .',
}

template2 = {
    'b': '{name} {vbd} what the {nn1} {vbd2} the {nn2} .',
    'g': '{name} {vbd} the {nn1} that the {nn2} {vbd2} .',
}


def main():
    """
    example:
    "sarah discovered the vase that the dog might take ." vs. "sarah discovered what the dog might take the vase ."

    """

    nouns_s = get_legal_words(tag='NN')

    excluded_verbs_base = ('put', 'run', 'say', 'be', 'give', 'tell', 'live')
    verbs_base = get_legal_words(tag='VB', exclude=excluded_verbs_base)

    excluded_verbs_past = ('started', 'let', 'told')
    verbs_past = get_legal_words(tag='VBD', exclude=excluded_verbs_past)

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    def add_preposition_after_vb(v: str):
        if v == 'play':
            return 'play with'
        elif v == 'point':
            return 'point to'
        elif v == 'turn':
            return 'turn to'
        elif v == 'work':
            return 'work with'
        else:
            return v

    while True:

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn1': random.choice(nouns_s),
            'nn2': random.choice(animates),
            'vbd': random.choice(verbs_past),
            'vbd2': random.choice(verbs_past),  # used in template2 only
            'vb': random.choice(verbs_base),  # used in template 1 only
        }

        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'])

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
