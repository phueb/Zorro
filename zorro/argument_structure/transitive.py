import random


from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': '{nn1} {vbz_or_vbd_transitive} .',
    'g': '{nn1} {vbz_or_vbd_intransitive} .',
}

template2 = {
    'b': '{aux} {nn1} {vb_transitive} ?',
    'g': '{aux} {nn1} {vb_intransitive} ?',
}


def main():
    """
    example:
    "sarah laughs" vs. "sarah gives"
    """

    # we need a lot of verbs here, so temporarily reduce restrictions imposed by counterbalancing
    tmp1 = configs.Data.tag2num_words['VB']
    tmp2 = configs.Data.tag2num_words['VBZ']
    tmp3 = configs.Data.tag2num_words['VBD']
    tmp4 = configs.Data.bias_tolerance
    configs.Data.tag2num_words['VB'] = 30
    configs.Data.tag2num_words['VBZ'] = 50
    configs.Data.tag2num_words['VBD'] = 50
    configs.Data.bias_tolerance = 7000

    vbs = get_legal_words(tag='VB', exclude=('fit', 'come', 'point'))
    vbzs = get_legal_words(tag='VBZ', exclude=('points', ))
    vbds = get_legal_words(tag='VBD', exclude=('fit', 'dropped', 'signed', 'formed', 'managed'))

    configs.Data.tag2num_words['VB'] = tmp1
    configs.Data.tag2num_words['VBZ'] = tmp2
    configs.Data.tag2num_words['VBD'] = tmp3
    configs.Data.bias_tolerance = tmp4

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    prps_s = ['she', 'he', 'it']
    prps_p = ['we', 'they']
    prps = prps_s + prps_p

    aux_s = ['does']
    auxiliaries = ['could', 'can', 'would', 'will', 'did'] + aux_s

    determiners = ['the', 'this', 'some', 'that', 'every'] + ['your', 'his', 'her']

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    vbs_intransitive = [
        'run',
        'work',
        'turn',
        'eat',
        'live',
        'read',
        'trade',
        'play',
        'know',
        'study',
        'think',
        'change',
    ]

    vbzs_intransitive = [
        'moves',
        'lives',
        'lies',
        'knows',
        'waves',
        'changes',
        'works',
        'dies',
        'leads',
        'appears',
        'thinks',
        'falls',
        'matters',
        'turns',
        'stands',
        'stands',
        'runs',
        'calls',
        'races',
    ]

    vbds_intransitive = [
        'occurred',
        'married',
        'moved',
        'looked',
        'changed',
        'finished',
        'grew',
        'broke',
        'started',
        'improved',
        'worked',
        'thought',
        'came',
        'tried',
        'read',
        'lost',
        'knew',
        'lived',
        'accepted',
        'developed',
        'joined',
        'joined',
        'decided',
        'learned',
        'occurred',
        'happened',
        'fell',
        'refused',
        'returned',
    ]

    vbs_intransitive = vbs_intransitive
    vbs_transitive = [v for v in vbs if v not in vbs_intransitive]

    vbzs_transitive = [v for v in vbzs if v not in vbzs_intransitive]

    vbzs_or_vbds_intransitive = vbzs_intransitive + vbds_intransitive
    vbzs_or_vbds_transitive = [v for v in vbzs + vbds if v not in vbzs_or_vbds_intransitive]

    while True:

        # random choices
        slot2filler = {
            'nn1': random.choice(animates + names + prps),
            'aux': random.choice(auxiliaries),
            'vbz_or_vbd_intransitive': random.choice(vbzs_or_vbds_intransitive),
            'vbz_or_vbd_transitive': random.choice(vbzs_or_vbds_transitive),
            'vb_intransitive': random.choice(vbs_intransitive),
            'vb_transitive': random.choice(vbs_transitive),
        }

        # handle exception: "occurred" and "happened" cannot have animate subject
        if slot2filler['vbz_or_vbd_intransitive'] in ['occurred', 'happened'] and\
                slot2filler['nn1'] not in ['it', 'that', 'this']:
            continue

        # add determiner to animate noun
        if slot2filler['nn1'] in animates:
            slot2filler['nn1'] = random.choice(determiners) + ' ' + slot2filler['nn1']

        # do not use template 1 with plural pronoun and VBZ
        if not (slot2filler['nn1'] in prps_p and
                slot2filler['vbz_or_vbd_intransitive'] in vbzs_intransitive or
                slot2filler['vbz_or_vbd_transitive'] in vbzs_transitive):

            yield template1['b'].format(**slot2filler)  # bad
            yield template1['g'].format(**slot2filler)  # good

        # do not use template 2 with plural pronoun and singular aux (e.g. "does")
        if not (slot2filler['nn1'] in prps_p and
                slot2filler['aux'] in aux_s):

            yield template2['b'].format(**slot2filler)  # bad
            yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
