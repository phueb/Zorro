
from zorro.agreement_in_1_verb_question.shared import paradigm, plural
from zorro.agreement_in_1_verb_question.shared import copulas_plural, copulas_singular
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words

NUM_NOUNS = 100

template1 = 'where {} the {} ?'
template2 = 'what {} the {} ?'
template3 = '{} the {} here ?'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('is', '{}'),
    ],
}


def main():
    """
    example:
    "where is the house?" vs "where is the houses?"
    todo "where is the house?" vs "where are the house?"
    """
    noun_plurals = get_vocab_words(tag='NNS')

    for copula in copulas_plural + copulas_singular:

        for (noun_s,) in get_task_word_combo(paradigm, rules.keys()):
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            yield template1.format(copula, noun_s)
            yield template1.format(copula, noun_p)

            yield template2.format(copula, noun_s)
            yield template2.format(copula, noun_p)

            yield template3.format(copula, noun_s)
            yield template3.format(copula, noun_p)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
