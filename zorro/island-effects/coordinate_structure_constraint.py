import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'who must {name} {vb} and the {nn} ?',
    'g': 'who must {name} and the {nn} {vb} ?',
}

template2 = {
    'b': 'who were {name} {vb} and the {nn} ?',
    'g': 'who were {name} and the {nn} {vbg} ?',
}

template3 = {
    'b': 'what did {name} {vb} and the {nn} ?',
    'g': 'what did {name} and the {nn} {vb} ?',
}

template4 = {
    'b': 'what were {name} {vbg} and the {nn} ?',
    'g': 'what were {name} and the {nn} {vbg} ?',
}

plural = inflect.engine()


def main():
    """
    example:
    "who must sarah and the dog kiss ?" vs "who must sarah kiss and the dog ?"

    """

    excluded_verbs_base = ('run', 'be', 'live', 'force', 'order')
    verbs_base = get_legal_words(tag='VB', exclude=excluded_verbs_base)

    excluded_verbs_gerund = ('',)
    verbs_gerund = get_legal_words(tag='VBG', exclude=excluded_verbs_gerund)

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    def add_preposition_after_vb(v: str,
                                 arg: str,
                                 ):
        if v == 'related':
            return 'related to'
        elif v == 'put':
            return 'put on'
        elif v == 'work':
            return 'work for'
        elif v == 'acting':
            return 'acting like'
        elif v == 'sleeping':
            return 'sleeping in'
        elif v == 'falling':
            return 'falling on'
        elif v == 'looking':
            return 'looking for'
        elif v == 'running':
            return 'running to'
        elif v == 'talking':
            return 'talking about'
        elif v == 'thinking':
            return 'thinking about'
        elif v == 'reaching':
            return 'reaching for'
        elif v == 'work':
            return f'work {arg}'
        else:
            return v

    while True:

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(animates),
            'vb': random.choice(verbs_base),
            'vbg': random.choice(verbs_gerund),
        }

        arg = random.choice(["him", "her", "them", "us"])
        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'], arg)
        slot2filler['vbg'] = add_preposition_after_vb(slot2filler['vbg'], arg)

        # exclude bad combinations that involve "who", e.g. "saying who"
        if slot2filler['vbg'] not in {'saying', 'drinking', 'eating', 'open'}\
                and slot2filler['vb'] not in {'need', 'feel', 'open'}:

            if slot2filler['vb'] == 'tell':
                slot2filler['vb'] = 'tell something'

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
