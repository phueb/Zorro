
from zorro.task_words import get_task_word_combo
from zorro.agreement_across_PP.shared import task_name, plural, copulas_singular, copulas_plural
from zorro.vocab import get_vocab_words

NUM_NOUNS = 50
NUM_ADJECTIVES = 20

template1 = 'the {} on the {} {} {} .'
template2 = 'the {} by the {} {} {} .'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('{}', '_', 'is', '_'),
        template2.format('{}', '_', 'is', '_'),
    ],
    ('NN', 1, NUM_NOUNS): [
        template1.format('_', '{}', 'is', '_'),
        template2.format('_', '{}', 'is', '_'),
    ],
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('_', '_', 'is/are', '{}'),
        template2.format('_', '_', 'is/are', '{}'),
    ],

}


def main():
    """
    example:
    "the dog on the mats is brown" vs "the dog on the mats are brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of sentences containing plural vs. singular object nouns
    2. subject with object number is counterbalanced such that:
        -singular subjects occur with 50:50 singular:plural objects
        -plural   subjects occur with 50:50 singular:plural objects
    """

    noun_plurals = get_vocab_words(tag='NNS')

    for copula in copulas_singular + copulas_plural:

        for sub_s, obj_s, adj in get_task_word_combo(task_name, rules.keys()):

            # counter-balance singular vs plural with subj vs. obj
            sub_p = plural.plural(sub_s)
            obj_p = plural.plural(obj_s)
            if sub_p not in noun_plurals or obj_p not in noun_plurals:
                continue
            if sub_s == sub_p or obj_s == obj_p:  # exclude nouns with ambiguous number
                continue

            # TEMPLATE 1

            # contrast is in number agreement between subject and copula
            yield template1.format(sub_s, obj_s, copula, adj)
            yield template1.format(sub_p, obj_s, copula, adj)

            # same as above, except that object number is opposite
            yield template1.format(sub_s, obj_p, copula, adj)
            yield template1.format(sub_p, obj_p, copula, adj)

            # TEMPLATE 2

            # contrast is in number agreement between subject and copula
            yield template2.format(sub_s, obj_s, copula, adj)
            yield template2.format(sub_p, obj_s, copula, adj)

            # same as above, except that object number is opposite
            yield template2.format(sub_s, obj_p, copula, adj)
            yield template2.format(sub_p, obj_p, copula, adj)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
