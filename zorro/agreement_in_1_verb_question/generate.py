import random

NUM_NOUNS = 90
NUM_ADJECTIVES = 50

template1 = 'where {} the {} ?'
template2 = 'what {} the {} ?'
template3 = 'what {} wrong with the {} ?'
template4 = '{} the {} not {} ?'
template5 = '{} the {} where it should be ?'
template6 = '{} the {} where they should be ?'
template7 = '{} the {} something you like ?'
template8 = '{} the {} a good idea ?'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('is', '{}'),
    ],
    ('JJ', 0, NUM_ADJECTIVES): [
            template4.format('is', '_', '{}'),
        ],
}


def main():
    """
    example:
    "where is the house?" vs "where is the houses?"
    todo "where is the house?" vs "where are the house?"
    """

    from zorro.agreement_in_1_verb_question.shared import paradigm, plural
    from zorro.agreement_in_1_verb_question.shared import copulas_plural, copulas_singular
    from zorro.task_words import get_task_words
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    nouns_s = get_task_words(paradigm, tag='NN', num_words_in_sample=NUM_NOUNS)
    adjectives = get_task_words(paradigm, tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            noun_s = random.choice(nouns_s)
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            # random choices
            copula = random.choice(copulas_singular + copulas_plural)
            adj = random.choice(adjectives)

            yield template1.format(copula, noun_s)
            yield template1.format(copula, noun_p)

            yield template2.format(copula, noun_s)
            yield template2.format(copula, noun_p)

            yield template3.format(copula, noun_s)
            yield template3.format(copula, noun_p)

            yield template4.format(copula, noun_s, adj)
            yield template4.format(copula, noun_p, adj)

            if copula in copulas_singular:
                yield template5.format(copula, noun_s)
                yield template5.format(copula, noun_p)
            else:
                yield template6.format(copula, noun_s)
                yield template6.format(copula, noun_p)

            yield template7.format(copula, noun_s)
            yield template7.format(copula, noun_p)

            yield template8.format(copula, noun_s)
            yield template8.format(copula, noun_p)

    # only collect unique sentences
    sentences = set()
    gen = gen_sentences()
    while len(sentences) // 2 < configs.Data.num_pairs_per_paradigm:
        sentence = next(gen)
        if sentence not in sentences:
            yield sentence
        sentences.add(sentence)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
