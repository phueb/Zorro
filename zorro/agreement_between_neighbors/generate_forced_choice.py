
from zorro.agreement_between_neighbors.shared import task_name, plural, pre_nominals_plural, pre_nominals_singular
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words

NUM_NOUNS = 1000

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
    noun_plurals = get_vocab_words(tag='NNS')

    for pre_nominal in pre_nominals_plural + pre_nominals_singular:

        for (noun_s,) in get_task_word_combo(task_name, rules.keys()):
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            yield template1.format(pre_nominal, noun_s)
            yield template1.format(pre_nominal, noun_p)

            yield template2.format(pre_nominal, noun_s)
            yield template2.format(pre_nominal, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
