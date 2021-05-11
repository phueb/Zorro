import random

NUM_NOUNS = 100

template1 = '{} {} must be here .'
template2 = '{} {} can be here .'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('one', '{}'),
        template2.format('one', '{}'),
    ],
}


def main():
    """
    example:
    "look at this house" vs. "look at this houses"
    """

    from zorro.agreement_between_neighbors.shared import paradigm, plural, pre_nominals_plural, pre_nominals_singular
    from zorro.task_words import get_task_words
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    nouns_s = get_task_words(paradigm, tag='NN')

    num_pairs = 0

    while num_pairs < configs.Data.num_pairs_per_paradigm:

        noun_s = random.choice(nouns_s)
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals or noun_p == noun_s:
            continue

        # random choices
        pre_nominal = random.choice(pre_nominals_singular + pre_nominals_plural)

        yield template1.format(pre_nominal, noun_s)
        yield template1.format(pre_nominal, noun_p)

        yield template2.format(pre_nominal, noun_s)
        yield template2.format(pre_nominal, noun_p)

        num_pairs += 2


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2:>12,}', s)
