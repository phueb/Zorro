import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'the {jj} {nn} {vbz1} {prp_obj} .',  # works with "give" only
    'g': '{vb1} {prp_obj} the {jj} {nn} .',
}

template2 = {
    'b': 'the {nn} {vbz2} {prp_obj} about .',  # works with "asks", "tells" only
    'g': '{vb2} {prp_obj} about the {nn} .',
}

template3 = {
    'b': '{det} {nn} {vbz3} {foil} .',  # works with "looks", "talks", etc
    'g': '{det} {nn} {vbz3} {filler} .',
}


plural = inflect.engine()


def main():
    """
    example:
    "give me the frog ." vs. "the frog gives me ."
    """

    # counterbalance both forms of verb as different forms are the contrast
    vbs_and_vbzs_1 = [
        ('give', 'gives'),
    ]

    vbs_and_vbzs_2 = [
        ('ask', 'asks'),
        ('tell', 'tells'),
    ]

    vbzs3_and_fillers_and_foils = [
        ('looks', 'well', 'like'),
        ('talks', 'quickly', 'about'),
        ('eats', 'everything', 'some'),
        ('plays', 'ball', 'with'),
        ('sleeps', 'here', 'on'),
        ('drinks', 'juice', 'the'),
        ('thinks', 'a lot', 'about many'),
        ('moves', 'fast', 'to'),
        ('works', 'hard', 'when'),
    ]

    adjectives = get_legal_words(tag='JJ')

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    personal_pronouns_obj = ['me', 'him', 'her', 'us', 'them']  # in the objective case
    personal_pronouns_subj = ['i', 'he', 'she', 'we', 'they']  # in the subjective case

    determiners = ['a', 'one', 'this', 'that', 'the', 'my', 'his', 'her']

    vowels = {'a', 'e', 'i', 'o', 'u'}

    while True:

        vb1, vbz1 = random.choice(vbs_and_vbzs_1)    # template 1
        vb2, vbz2 = random.choice(vbs_and_vbzs_2)    # template 2
        vbz3, filler, foil = random.choice(vbzs3_and_fillers_and_foils)    # template 3

        # random choices
        slot2filler = {
            'det': random.choice(determiners),
            'jj': random.choice(adjectives),
            'nn': random.choice(animates),
            'nn2': random.choice(nouns_s),
            'prp_obj': random.choice(personal_pronouns_obj),
            'prp_subj': random.choice(personal_pronouns_subj),
            'vb1': vb1,
            'vbz1': vbz1,
            'vb2': vb2,
            'vbz2': vbz2,
            'vbz3': vbz3,
            'filler': filler,
            'foil': foil,
        }

        if slot2filler['det'] == 'a' and slot2filler['nn2'][0] in vowels:
            slot2filler['det'] += 'n'

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good

        yield template3['b'].format(**slot2filler)  # bad
        yield template3['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
