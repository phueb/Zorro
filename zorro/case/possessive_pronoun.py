import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words


template1 = {
    'b': '{prp_subj} can {vb} {prp_poss} .',  # possessive case is wrong
    'g': '{prp_subj} can {vb} {prp_obj} .',
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
    print(verbs_base)

    nouns_s = get_legal_words(tag='NN')

    prps_obj_and_ref = [
        ('him', 'himself'),
        ('her', 'herself'),
    ]

    personal_pronouns_subj = ['i', 'you', 'we', 'they']  # exclude 3rd person

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

        prp_obj, prp_ref = random.choice(prps_obj_and_ref)    # template 1

        # sample argument once, so that the same argument is used by both bad and good sentences.
        # note: pronouns don't get determiners, but nouns do
        argument1 = random.choice([f'the {nn}' for nn in nouns_s[:10]])

        # random choices
        slot2filler = {
            'prp_ref':  prp_ref,
            'prp_obj':  prp_obj,
            'prp_subj': random.choice(personal_pronouns_subj),
            'vb': random.choice(verbs_base),
        }

        # first, add some miscellaneous component
        slot2filler['prp_ref'] = add_misc(slot2filler['vb'], prp_ref, argument1)
        slot2filler['prp_obj'] = add_misc(slot2filler['vb'], prp_obj, argument1)

        # lastly, add a preposition
        slot2filler['vb'] = add_preposition_after_vb(slot2filler['vb'])

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
