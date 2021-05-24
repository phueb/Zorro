import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.words import get_legal_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

template1 = {
    'b': '{det} {nn} {aux} ever {vb} ?',
    'g': '{aux} {det} {nn} ever {vb} ?',
}

template2 = {
    'b': '{name} {aux} ever {vb} ?',
    'g': '{aux} {name} ever {vb} ?',
}


plural = inflect.engine()


def main():
    """
    example:
    "has sam ever worried sarah ?" vs. "jane has ever worried sarah ."
    """

    vbs = get_legal_words(tag='VB')

    nouns_s = get_legal_words(tag='NN')

    animates_ = (configs.Dirs.legal_words / 'animates.txt').open().read().split()
    animates = find_counterbalanced_subset(animates_, min_size=8, max_size=len(animates_))

    names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()
    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    auxiliaries = ['does', 'will', 'could', 'did', 'should', 'would']

    determiners = ['a', 'the', 'this', 'some', 'that'] + ['your', 'his', 'her']

    def add_argument_after_vb(v: str,
                              arg1: str,
                              arg2: str,
                              ) -> str:
        if v in {'say'}:
            return f'{v} something'
        elif v in {'read'}:
            return f'{v} a book'
        elif v in {'play'}:
            return f'{v} with {arg1}'
        elif v in {'use', 'find', 'get', 'be', 'order', 'need', 'have', 'control', 'want', 'free', 'keep'}:
            return f'{v} {arg1}'
        elif v in {'tell'}:
            return f'{v} me about {arg1}'
        elif v in {'plan'}:
            return f'{v} to do something with {arg1}'
        elif v in {'take'}:
            return f'{v} {arg1} away'
        elif v in {'give', 'show', 'present'}:
            return f'{v} {arg1} to {arg2}'
        elif v in {'put'}:
            return f'{v} {arg1} on {arg2}'
        elif v in {'fall'}:
            return f'{v} in {arg1}'
        elif v in {'see'}:
            return f'{v} how the {arg1} works'
        elif v in {'come'}:
            return f'{v} to {arg1}'
        else:
            return v

    while True:

        # sample argument once, so that the same argument is used by both bad and good sentences.
        # note: pronouns don't get determiners, but nouns do
        argument1 = random.choice(['you', 'him', 'her', 'it'] + [f'the {nn}' for nn in nouns_s])
        argument2 = random.choice(['you', 'him', 'her', 'it'] + [f'the {nn}' for nn in nouns_s])

        vb = random.choice(vbs)

        # random choices
        slot2filler = {
            'name': random.choice(names),
            'nn': random.choice(animates),
            'vb': add_argument_after_vb(vb, argument1, argument2),
            'aux': random.choice(auxiliaries),
            'det': random.choice(determiners),
        }

        if slot2filler['aux'] in {'did', 'does'} and vb == 'be':
            continue

        yield template1['b'].format(**slot2filler)  # bad
        yield template1['g'].format(**slot2filler)  # good

        yield template2['b'].format(**slot2filler)  # bad
        yield template2['g'].format(**slot2filler)  # good


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
