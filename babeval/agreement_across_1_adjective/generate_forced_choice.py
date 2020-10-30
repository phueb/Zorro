
from babeval.agreement_across_1_adjective.shared import task_name, plural, pre_nominals_singular, pre_nominals_plural
from babeval.task_words import get_task_word_combo
from babeval.whole_words import get_whole_words

NUM_ADJECTIVES = 2
NUM_NOUNS = 6

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

    noun_plurals = get_whole_words(tag='NNS')

    for pre_nominal in pre_nominals_singular + pre_nominals_plural:

        for words_singular in get_task_word_combo(task_name, rules.keys()):
            noun_plural = plural.plural(words_singular[1])
            if noun_plural not in noun_plurals:
                continue
            words_plural = [words_singular[0], noun_plural]

            yield template1.format(pre_nominal, *words_singular)
            yield template1.format(pre_nominal, *words_plural)

            yield template2.format(pre_nominal, *words_singular)
            yield template2.format(pre_nominal, *words_plural)


if __name__ == '__main__':
    for s in main():
        print(s)
