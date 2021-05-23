import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': 'the {nn} {vbd} {prp_subj} {det} {nn2} .',  # subjective pronoun is wrong
    'g': '{prp_subj} {vbd} the {nn} {det} {nn2} .',
}

plural = inflect.engine()


def main():
    """
    example:
    "he made the van this challenge ." vs. "the van made he this challenge ."
    """

    # counterbalance both forms of verb as different forms are the contrast

    vbds = [
        'brought',
        'made',
        'built',
        'gave',
        'showed',
    ]

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    personal_pronouns_obj = ['me', 'him', 'her', 'us', 'them']  # in the objective case
    personal_pronouns_subj = ['i', 'he', 'she', 'we', 'they']  # in the subjective case

    determiners = ['a', 'one', 'this', 'that', 'the', 'my', 'his', 'her']

    vowels = {'a', 'e', 'i', 'o', 'u'}

    while True:

        vbd = random.choice(vbds)    # template 1

        # random choices
        slot2filler = {
            'nn': random.choice(animates),
            'nn2': random.choice(nouns_s),
            'det': random.choice(determiners),
            'prp_obj': random.choice(personal_pronouns_obj),
            'prp_subj': random.choice(personal_pronouns_subj),
            'vbd': vbd,
        }

        if slot2filler['det'] == 'a' and slot2filler['nn2'][0] in vowels:
            slot2filler['det'] += 'n'

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
