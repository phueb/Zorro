
from zorro.agreement_in_2_verb_question.shared import paradigm, plural
from zorro.agreement_in_2_verb_question.shared import doing_plural, doing_singular
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words

NUM_NOUNS = 100

template1 = 'where {} the {} go ?'
template2 = 'what {} the {} do ?'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('does', '{}'),
        template2.format('does', '{}'),
    ],
}


def main():
    """
    example:
    "where does the dog go?"
    "what does the dog do?"
    """
    noun_plurals = get_vocab_words(tag='NNS')

    for doing in doing_plural + doing_singular:

        for (noun_s,) in get_task_word_combo(paradigm, rules.keys()):
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            yield template1.format(doing, noun_s)
            yield template1.format(doing, noun_p)

            yield template2.format(doing, noun_s)
            yield template2.format(doing, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
