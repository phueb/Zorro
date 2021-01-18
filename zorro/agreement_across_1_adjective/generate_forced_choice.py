
from zorro.agreement_across_1_adjective.shared import task_name, plural, pre_nominals_singular, pre_nominals_plural
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words

NUM_ADJECTIVES = 50
NUM_NOUNS = 300

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

    noun_plurals = get_vocab_words(tag='NNS')

    for pre_nominal in pre_nominals_singular + pre_nominals_plural:

        for adj, noun_s in get_task_word_combo(task_name, rules.keys()):
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            yield template1.format(pre_nominal, adj, noun_s)
            yield template1.format(pre_nominal, adj, noun_p)

            yield template2.format(pre_nominal, adj, noun_s)
            yield template2.format(pre_nominal, adj, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
