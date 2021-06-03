import random


from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.gender import names_f, names_m

# past tense

template1 = {
    'b': '{nn_m} {vb} himself {vbd1} {det} {nn2} .',
    'g': '{nn_m} {vb} himself {vbg1} {det} {nn2} .',
}

template2 = {
    'b': '{nn_f} {vb} herself {vbd1} {det} {nn2} .',
    'g': '{nn_f} {vb} herself {vbg1} {det} {nn2} .',
}

# present tense

template3 = {
    'b': '{nn_m} {vb} himself {vbz2} {det} {nn2} .',
    'g': '{nn_m} {vb} himself {vbg2} {det} {nn2} .',
}

template4 = {
    'b': '{nn_f} {vb} herself {vbz2} {det} {nn2} .',
    'g': '{nn_f} {vb} herself {vbg2} {det} {nn2} .',
}


def main():
    """
    example:
    "sarah thinks about herself listening to the dog." vs. "sarah thinks about herself listened to that girl.""
    """

    vbds1_and_vbgs1 = get_legal_words(tag='VBD', second_tag='VBG',
                                      exclude=('told', 'forgot', 'thought', 'said', 'happened'))

    vbzs2_and_vbgs2 = get_legal_words(tag='VBZ', second_tag='VBG',
                                      exclude=('tells', 'forgets', 'thinks', 'says', 'happens'))

    nouns_s = get_legal_words(tag='NN')

    vowels = {'a', 'e', 'i', 'o', 'u'}

    determiners = ['a', 'the', 'this', 'some', 'that']

    vbs = ['thinks about',
           'thought about',
           'did not think about',
           'could think about',
           'must think about',
           'must not think about',
           ]

    def add_preposition_after_vb(v: str) -> str:
        if v in {'falling', 'fell'}:
            return f'{v} on'
        elif v in {'came', 'come', 'comes', 'coming',
                   'went', 'go', 'goes', 'going',
                   'wrote', 'write', 'writes', 'writing',
                   'ran', 'run', 'runs', 'running',
                   }:
            return f'{v} to'
        elif v in {'lived', 'live', 'lives', 'living'}:
            return f'{v} in'
        elif v in {'looked', 'look', 'looks', 'looking'}:
            return f'{v} at'
        elif v in {'reached', 'reach', 'reaches', 'reaching'}:
            return f'{v} for'
        elif v in {'showed', 'show', 'shows', 'showing'}:
            return f'{v} off'
        elif v in {'set', 'sets', 'setting',}:
            return f'{v} up'
        elif v in {'put', 'puts', 'putting'}:
            return f'{v} away'
        else:
            return v

    while True:

        vbd1, vbg1 = random.choice(vbds1_and_vbgs1)
        vbz2, vbg2 = random.choice(vbzs2_and_vbgs2)

        # random choices
        slot2filler = {
            'nn_m': random.choice(names_m),
            'nn_f': random.choice(names_f),
            'nn2': random.choice(nouns_s),
            'vbd1': add_preposition_after_vb(vbd1),
            'vbg1': add_preposition_after_vb(vbg1),
            'vbz2': add_preposition_after_vb(vbz2),
            'vbg2': add_preposition_after_vb(vbg2),
            'vb': random.choice(vbs),
            'det': random.choice(determiners),
            'prp_reflexive_m': 'himself',
            'prp_reflexive_f': 'herself',
        }

        if slot2filler['det'] == 'a' and slot2filler['nn2'][0] in vowels:
            slot2filler['det'] += 'n'

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good

        yield template3['b'].format(**slot2filler)  # bad
        yield template3['g'].format(**slot2filler)  # good

        yield template4['b'].format(**slot2filler)  # bad
        yield template4['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
