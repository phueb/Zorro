import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 100

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'

rules = {
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('this', '{}', '_'),
        template2.format('this', '{}', '_'),
    ],
    ('NN', 0, NUM_NOUNS): [
        template1.format('this', '_', '{}'),
        template2.format('this', '_', '{}'),
    ],
}


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    "this green house went there ." vs. "this green houses went there."
    """

    from zorro.task_words import get_task_words
    from zorro.agreement_across_1_adjective.shared import paradigm, plural, pre_nominals_singular, pre_nominals_plural
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    adjectives = get_task_words(paradigm, tag='JJ')
    nouns_s = get_task_words(paradigm, tag='NN')

    num_pairs = 0

    while num_pairs < configs.Data.num_pairs_per_paradigm:

        noun_s = random.choice(nouns_s)
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals or noun_p == noun_s:
            continue

        # random choices
        pre_nominal = random.choice(pre_nominals_singular + pre_nominals_plural)
        adj = random.choice(adjectives)

        yield template1.format(pre_nominal, adj, noun_s)
        yield template1.format(pre_nominal, adj, noun_p)

        yield template2.format(pre_nominal, adj, noun_s)
        yield template2.format(pre_nominal, adj, noun_p)

        num_pairs += 2


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2:>12,}', s)
