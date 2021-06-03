import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro.gender import names_f, names_m
from zorro import configs

template1 = {
    'b': '{aux} {nn_m} {vb} {prp_f} ?',
    'g': '{aux} {nn_m} {vb} {prp_m} ?',
}

template2 = {
    'b': '{aux} {nn_f} {vb} {prp_m} ?',
    'g': '{aux} {nn_f} {vb} {prp_f} ?',
}

template3 = {
    'b': '{nn_m} {aux} {vb} {prp_f} .',
    'g': '{nn_m} {aux} {vb} {prp_m} .',
}

template4 = {
    'b': '{nn_f} {aux} {vb} {prp_m} .',
    'g': '{nn_f} {aux} {vb} {prp_f} .',
}



plural = inflect.engine()


def main():
    """
    example:
    "katherine will help herself do something" vs. "katerine will help himself do something"
    """

    excluded_verbs_base = ('say', )
    verbs_base = get_legal_words(tag='VB', exclude=excluded_verbs_base)

    nouns_s = get_legal_words(tag='NN')

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    auxiliaries = ['can', 'could', 'will', 'would', 'must', 'should']

    def add_misc_after_prp(prp: str,
                           v: str,
                           arg1: str,
                           ) -> str:

        if v in {'take', }:
            return f'{prp} to {arg1}'

        elif v in {'make', 'give', 'put'}:
            return f'{prp} {arg1}'

        elif v in {'work',}:
            return f'{prp} on {arg1}'

        elif v in {'turn', }:
            return f'{prp} around'

        elif v in {'tell', }:
            return f'{prp} about {arg1}'
        else:
            return prp

    def add_preposition_after_vb(v: str) -> str:
        if v in {'work', 'study', 'live'}:
            return f'{v} with'
        elif v in {'point', 'run'}:
            return f'{v} to'
        elif v in {'be', }:
            return f'{v} like'
        else:
            return v

    while True:

        vb = random.choice(verbs_base)

        # random choices
        slot2filler = {
            'aux': random.choice(auxiliaries),
            'nn_m': random.choice([name for name in names if name in names_m]),
            'nn_f': random.choice([name for name in names if name in names_f]),
        }

        # sample argument once, so that the same argument is used by both bad and good sentences.
        # note: pronouns don't get determiners, but nouns do
        if vb == 'put':
            argument1 = random.choice(['in danger', 'in this situation'])
        else:
            argument1 = random.choice([f'the {nn}' for nn in nouns_s])

        # first, add some miscellaneous component
        slot2filler['prp_m'] = add_misc_after_prp('himself', vb, argument1)
        slot2filler['prp_f'] = add_misc_after_prp('herself', vb, argument1)

        # second, add a preposition
        slot2filler['vb'] = add_preposition_after_vb(vb)

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good

        # use negation only in non-question, in templates 3, and 4
        if random.random() < 0.5:
            slot2filler['aux'] += ' ' + 'not'
        if random.random() < 0.1:
            slot2filler['aux'] = 'did not'

        yield template3['b'].format(**slot2filler)  # bad
        yield template3['g'].format(**slot2filler)  # good

        yield template4['b'].format(**slot2filler)  # bad
        yield template4['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
