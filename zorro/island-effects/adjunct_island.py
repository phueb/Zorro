import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'who should {name} {vb} the {nn} {pp} {vbg} ?',
    'g': 'who should {name} {vb} {pp} {vbg} the {nn} ?',
}

template2 = {
    'b': 'what did {name} {vb} the {nn} {pp} {vbg} ?',
    'g': 'what did {name} {vb} {pp} {vbg} the {nn} ?',
}

plural = inflect.engine()


def main():
    """
    example:
    "who should sarah hug after shocking the dog ?" vs "who should sarah hug the dog after shocking ?"

    """

    nouns_s = get_legal_words(tag='NN')

    excluded_verbs_present = ('run', 'say', 'be', 'give', 'tell', 'live', 'force')
    verbs_present = get_legal_words(tag='VB', exclude=excluded_verbs_present)

    excluded_verbs_gerund = ('saying', )
    verbs_gerund = get_legal_words(tag='VBG', exclude=excluded_verbs_gerund)

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    pps = ['after', 'before', 'while', 'without']

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

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(nouns_s),
            'pp': random.choice(pps),
            'vb': random.choice(verbs_present),
            'vbg': random.choice(verbs_gerund),
        }

        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'])
        slot2filler['vbg'] = add_preposition_after_vb(slot2filler['vbg'])

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
