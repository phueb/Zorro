import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'is the {nn} {vbz1} ?',
    'g': 'is the {nn} {vbg1} ?',
}

template2 = {
    'b': 'can the {nn} {vbz2} ?',
    'g': 'can the {nn} {vb2} ?',
}


plural = inflect.engine()


def main():
    """
    example:
    "is the bell ringing ?" vs "is the bell rings ?"
    """

    # counterbalance both forms of verb as different forms are the contrast
    vbgs_and_vbzs = get_legal_words(tag='VBG', second_tag='VBZ',
                                    exclude=('facing', 'naming', 'training', 'setting', 'meaning'))
    vbs_and_vbzs = get_legal_words(tag='VB', second_tag='VBZ')

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    def add_argument_after_vb(v: str,
                              arg1: str,
                              arg2: str,
                              ) -> str:
        if v in {'saying', 'says', 'say'}:
            return f'{v} something'
        elif v in {'using', 'uses', 'use'}:
            return f'{v} {arg1}'
        elif v in {'telling', 'tells', 'tell'}:
            return f'{v} me about {arg1}'
        elif v in {'making', 'makes', 'make'}:
            return f'{v} {arg1} something'
        elif v in {'planning', 'plans', 'plan'}:
            return f'{v} to do something with {arg1}'
        elif v in {'taking', 'takes', 'take'}:
            return f'{v} {arg1} away'
        elif v in {'giving', 'gives', 'give'}:
            return f'{v} {arg1} {arg2}'
        elif v in {'falling', 'falls', 'fall'}:
            return f'{v} in {arg1}'
        elif v in {'showing', 'shows', 'show'}:
            return f'{v} {arg1} to {arg2}'
        elif v in {'seeing', 'sees', 'see'}:
            return f'{v} how the {arg1} works'
        elif v in {'finding', 'finds', 'find'}:
            return f'{v} {arg1}'
        elif v in {'coming', 'comes', 'come'}:
            return f'{v} to {arg1}'
        elif v in {'getting', 'gets', 'get'}:
            return f'{v} {arg1}'
        elif v in {'depending', 'depends', 'depend'}:
            return f'{v} on {arg1}'
        else:
            return v

    while True:

        vbg1, vbz1 = random.choice(vbgs_and_vbzs)  # template 1
        vb2, vbz2 = random.choice(vbs_and_vbzs)    # template 2

        # sample argument once, so that the same argument is used by both bad and good sentences.
        # note: pronouns don't get determiners, but nouns do
        argument1 = random.choice(['you', 'him', 'her', 'it'] + [f'the {nn}' for nn in nouns_s[:10]])
        argument2 = random.choice(['you', 'him', 'her', 'it'] + [f'the {nn}' for nn in nouns_s[:10]])

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(nouns_s + animates),
            'vb2': add_argument_after_vb(vb2, argument1, argument2),
            'vbz2': add_argument_after_vb(vbz2, argument1, argument2),
            'vbg1': add_argument_after_vb(vbg1, argument1, argument2),
            'vbz1': add_argument_after_vb(vbz1, argument1, argument2),
        }

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
