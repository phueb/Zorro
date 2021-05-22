import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': '{name} {vbd} who the {nn} can {vb} {nns} .',
    'g': '{name} {vbd} the {nn} that can {vb} {nns} .',
}

template2 = {
    'b': '{name} {vbd} who the {nn} is {vbg} {nns} .',
    'g': '{name} {vbd} the {nn} that is {vbg} {nns} .',
}

plural = inflect.engine()


def main():
    """
    example:
    sam questioned the dog that can hurt sara ." vs "sam questioned who the dog can hurt sara."

    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN')
                     if plural.plural(noun_s) != noun_s]

    excluded_verbs_present = ('put', 'run', 'say', 'be', 'give', 'tell', 'live')
    verbs_present = get_legal_words(tag='VB', exclude=excluded_verbs_present)

    excluded_verbs_past = ('started', 'let', 'told')
    verbs_past = get_legal_words(tag='VBD', exclude=excluded_verbs_past)

    excluded_verbs_gerund = ('saying', )
    verbs_gerund = get_legal_words(tag='VBG', exclude=excluded_verbs_gerund)

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    def add_preposition_after_vb(v: str):
        if v == 'related':
            return 'related to'
        elif v == 'acting':
            return 'acting like'
        elif v == 'work':
            return 'work with'
        elif v == 'sleeping':
            return 'sleeping in'
        elif v == 'standing':
            return 'standing on'
        elif v == 'falling':
            return 'falling on'
        elif v == 'asking':
            return 'asking about'
        elif v == 'swimming':
            return 'swimming in'
        else:
            return v

    while True:

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(nouns_s_and_p)[0],
            'nns': random.choice(nouns_s_and_p)[1],
            'vbd': random.choice(verbs_past),
            'vbg': random.choice(verbs_gerund),  # used in template2 only
            'vb': random.choice(verbs_present),  # used in template 1 only
        }

        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'])
        slot2filler['vbd'] = add_preposition_after_vb(slot2filler['vbd'])
        slot2filler['vbg'] = add_preposition_after_vb(slot2filler['vbg'])

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
