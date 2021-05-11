import random

NUM_NOUNS = 90
NUM_ADJECTIVES = 50

template1 = 'where {} the {} go ?'
template2 = 'what {} the {} do ?'
template3 = 'how {} the {} fit in here ?'
template4 = 'how {} the {} become {} ?'
template5 = 'when {} the {} stop working ?'
template6 = 'when {} the {} start ?'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('does', '{}'),
        template2.format('does', '{}'),
    ],
    ('JJ', 0, NUM_ADJECTIVES): [
        template4.format('does', '_', '{}'),
    ],
}


def main():
    """
    example:
    "where does the dog go?"
    "what does the dog do?"
    """

    from zorro.agreement_in_2_verb_question.shared import paradigm, plural
    from zorro.agreement_in_2_verb_question.shared import doing_plural, doing_singular
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
            doing = random.choice(doing_singular + doing_plural)
            adj = random.choice(adjectives)

            yield template1.format(doing, noun_s)
            yield template1.format(doing, noun_p)

            yield template2.format(doing, noun_s)
            yield template2.format(doing, noun_p)

            yield template3.format(doing, noun_s)
            yield template3.format(doing, noun_p)

            yield template4.format(doing, noun_s, adj)
            yield template4.format(doing, noun_p, adj)

            yield template5.format(doing, noun_s)
            yield template5.format(doing, noun_p)

            yield template6.format(doing, noun_s)
            yield template6.format(doing, noun_p)

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
