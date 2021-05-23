import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset

template1 = {
    'b': 'the {nn} {aux} {vb} {prp_poss} .',  # possessive case is wrong
    'g': 'the {nn} {aux} {vb} {prp_obj} .',
}

plural = inflect.engine()


def main():
    """
    example:
    "we can help him do something" vs. "we can help himself do something"
    """

    # counterbalance both forms of verb as different forms are the contrast

    excluded_verbs_base = ('say', 'live')
    verbs_base = get_legal_words(tag='VB', exclude=excluded_verbs_base)

    nouns_s = get_legal_words(tag='NN')

    prps_obj_and_poss = [
        ('him', 'his'),
        ('her', 'hers'),
        ('us', 'our'),
        ('them', 'theirs'),
    ]

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    auxiliaries = ['can', 'could', 'will', 'would', 'must', 'should']

    def add_misc(v: str,
                 prp: str,
                 arg1: str,
                 ) -> str:
        if v in {'take'}:
            return f'{prp} to {arg1}'
        elif v in {'make'}:
            return f'{prp} do {arg1}'
        elif v in {'work', 'put'}:
            return f'{prp} on {arg1}'
        elif v in {'turn'}:
            return f'{prp} around'
        elif v in {'tell'}:
            return f'{prp} about {arg1}'
        else:
            return v

    def add_preposition_after_vb(v: str) -> str:
        if v in {'work', 'study'}:
            return f'{v} with'
        elif v in {'point', 'run'}:
            return f'{v} to'
        elif v in {'be'}:
            return f'{v} like'
        else:
            return v

    while True:

        prp_obj, prp_poss = random.choice(prps_obj_and_poss)

        # random choices
        slot2filler = {
            'aux':  random.choice(auxiliaries),
            'prp_poss':  prp_poss,
            'prp_obj':  prp_obj,
            'nn': random.choice(animates),
            'vb': random.choice(verbs_base),
        }

        # sample argument once, so that the same argument is used by both bad and good sentences.
        # note: pronouns don't get determiners, but nouns do
        argument1 = random.choice([f'the {nn}' for nn in nouns_s[:10]])

        # first, add some miscellaneous component
        slot2filler['prp_poss'] = add_misc(slot2filler['vb'], prp_poss, argument1)
        slot2filler['prp_obj'] = add_misc(slot2filler['vb'], prp_obj, argument1)

        # lastly, add a preposition
        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'])

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
