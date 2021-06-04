import random

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'the {jj} {nn} {vbz1} {prp_obj} .',  # works with "give" only
    'g': '{vb1} {prp_obj} the {jj} {nn} .',
}

template2 = {
    'b': 'the {nn} {vbz2} {prp_obj} about .',  # works with "asked", "tells" only
    'g': '{vb2} {prp_obj} about the {nn} .',
}

template3 = {
    'b': '{det} {nn} {vbz3} {cont_b} .',  # works with many other verbs
    'g': '{det} {nn} {vbz3} {cont_g} .',
}


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
        ('ask', 'asked'),  # "asks" is not in vocab
        ('tell', 'tells'),
    ]

    prps_obj = ['me', 'you', 'him', 'her', 'them']

    conjunctions = ['when', 'but', 'with', 'and']

    # TODO use a counterbalanced verb list

    vbzs3_and_continuations = [  # contains a mix of past and present tense forms
        # past tense form
        ('saw', '{prp_obj} there', '{prp_obj} by'),
        ('created', '{prp_obj}', '{det}'),
        ('told', '{prp_obj} about that', '{prp_obj} about {det}'),
        ('wrote', '{prp_obj} something', '{prp_obj} {det}'),
        ('wanted', '{prp_obj}', 'to'),
        ('asked', 'about {prp_obj}', '{prp_obj} about'),
        ('sold', '{prp_obj} that', 'that to'),
        ('changed', '{prp_obj}', '{det}'),
        # present tense form
        ('looks', 'at {prp_obj}', 'at {det}'),
        ('plays', 'with {prp_obj}', 'with {det}'),
        ('thinks', 'about {prp_obj}', 'about {det}'),
        ('moves', 'fast', 'to'),
        ('works', 'well', '{conjunction}'),
    ]

    adjectives = get_legal_words(tag='JJ')

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    personal_pronouns_obj = ['me', 'him', 'her', 'us', 'them']  # in the objective case
    personal_pronouns_subj = ['i', 'he', 'she', 'we', 'they']  # in the subjective case

    determiners = ['a', 'one', 'the', 'my', 'his', 'some']  # do not include "this" or "that" or "her"

    vowels = {'a', 'e', 'i', 'o', 'u'}

    while True:

        vb1, vbz1 = random.choice(vbs_and_vbzs_1)    # template 1
        vb2, vbz2 = random.choice(vbs_and_vbzs_2)    # template 2
        vbz3, cont_g, cont_b = random.choice(vbzs3_and_continuations)    # template 3

        # good and bad continuations
        prp_obj = random.choice(prps_obj)
        conjunction = random.choice(conjunctions)
        cont_g = cont_g.format(prp_obj=prp_obj)
        cont_b = cont_b.format(prp_obj=prp_obj, det=random.choice(determiners), conjunction=conjunction)

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
            'cont_g': cont_g,
            'cont_b': cont_b,
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
