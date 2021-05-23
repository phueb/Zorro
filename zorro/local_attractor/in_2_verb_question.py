import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'is the {nn} {vbg} ?',
    'g': 'is the {nn} {vbz} ?',
}

template2 = {
    'b': 'does the {nn} {vb} ?',
    'g': 'does the {nn} {vbz} ?',
}


plural = inflect.engine()


def main():
    """
    example:
    "is the bell ringing ?" vs "is the bell rings ?"


    """

    # counterbalance all forms of verb as different forms are the contrast
    vbgs_and_vbzs = get_legal_words(tag='VBG', second_tag='VBZ')
    print(vbgs_and_vbzs)

    nouns_s = get_legal_words(tag='NN')

    # excluded_verbs_3p = ('', )
    # verbs_3p = get_legal_words(tag='VBZ', exclude=excluded_verbs_3p)
    #
    # excluded_verbs_gerund = ('saying', )
    # verbs_gerund = get_legal_words(tag='VBG', exclude=excluded_verbs_gerund)

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))


    def add_preposition_after_vb(v: str):
        if v == 'related':
            return 'related to'
        elif v == 'acting':
            return 'acting like'
        elif v == 'put':
            return 'put on'
        elif v == 'work':
            return 'work for'
        elif v == 'sleeping':
            return 'sleeping in'
        elif v == 'standing':
            return 'standing on'
        elif v == 'depending':
            return 'depending on'
        elif v == 'flying':
            return 'flying over'
        elif v == 'falling':
            return 'falling on'
        elif v == 'asking':
            return 'asking about'
        elif v == 'swimming':
            return 'swimming in'
        elif v == 'asking':
            return 'asking for'
        elif v == 'coming':
            return 'coming to'
        else:
            return v

    while True:

        vbg, vbz = random.choice(vbgs_and_vbzs)

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(nouns_s),
            'vbg': vbg,
            'vbz': vbz,
        }

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        # yield template2['b'].format(**slot2filler)  # bad
        # yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
