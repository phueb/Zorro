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
    vbs_and_vbzs = get_legal_words(tag='VB', second_tag='VBZ',
                                   )

    nouns_s = get_legal_words(tag='NN')

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    def add_argument_after_vb(v: str):
        if v in {'saying', 'says', 'say'}:
            return v + ' ' + 'something'
        elif v in {'using', 'uses', 'use'}:
            return v + ' ' + 'the' + ' ' + random.choice(nouns_s)
        elif v in {'telling', 'tells', 'tell'}:
            return v + ' ' + 'me about the' + ' ' + random.choice(nouns_s)
        elif v in {'making', 'makes', 'make'}:
            return v + ' ' + 'the' + ' ' + random.choice(nouns_s)
        elif v in {'planning', 'plans', 'plan'}:
            return v + ' ' + 'to do something'
        elif v in {'taking', 'takes', 'take'}:
            return v + ' ' + 'the' + ' ' + random.choice(nouns_s) + ' ' + 'away'
        elif v in {'giving', 'gives', 'give'}:
            return v + ' ' + 'you the ' + random.choice(nouns_s)
        elif v in {'falling', 'falls', 'fall'}:
            return v + ' ' + 'in the ' + random.choice(nouns_s)
        elif v in {'showing', 'shows', 'show'}:
            return v + ' ' + 'you the ' + random.choice(nouns_s)
        elif v in {'seeing', 'sees', 'see'}:
            return v + ' ' + 'how the' + random.choice(nouns_s) + ' ' + 'works'
        elif v in {'finding', 'finds', 'find'}:
            return v + ' ' + random.choice(['you', 'him', 'her', 'it'])
        elif v in {'coming', 'comes', 'come'}:
            return v + ' ' + 'to the' + ' ' + random.choice(nouns_s)
        elif v in {'getting', 'gets', 'get'}:
            return v + ' ' + random.choice(['you', 'him', 'her', 'it'])
        elif v in {'depending', 'depends', 'depend'}:
            return v + ' ' + 'on' + ' ' + random.choice(['you', 'him', 'her', 'it'])
        else:
            return v

    while True:

        vbg1, vbz1 = random.choice(vbgs_and_vbzs)  # template 1
        vb2, vbz2 = random.choice(vbs_and_vbzs)    # template 2

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(nouns_s),
            'vb2': add_argument_after_vb(vb2),
            'vbz2': add_argument_after_vb(vbz2),
            'vbg1': add_argument_after_vb(vbg1),
            'vbz1': add_argument_after_vb(vbz1),
        }

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
