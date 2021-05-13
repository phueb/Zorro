import random

NUM_NOUNS = 20
NUM_ADJECTIVES = 50

template1 = '{} {} must be {} .'
template2 = '{} {} can be {} .'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('one', '{}', 'here'),
        template2.format('one', '{}', 'here'),
    ],
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('one', 'thing', '{}'),
        template2.format('one', 'thing', '{}'),
    ],
}


def main():
    """
    example:
    "look at this house" vs. "look at this houses"
    """

    from zorro.agreement_between_neighbors.shared import paradigm, plural, pre_nominals_plural, pre_nominals_singular
    from zorro.words import get_words_for_paradigm
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    nouns_s = get_words_for_paradigm(paradigm, tag='NN', num_words_in_sample=NUM_NOUNS)
    adjectives = get_words_for_paradigm(paradigm, tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            noun_s = random.choice(nouns_s)
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            # random choices
            pre_nominal = random.choice(pre_nominals_singular + pre_nominals_plural)
            adj = random.choice(adjectives)

            yield template1.format(pre_nominal, noun_s, adj)
            yield template1.format(pre_nominal, noun_p, adj)

            yield template2.format(pre_nominal, noun_s, adj)
            yield template2.format(pre_nominal, noun_p, adj)

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
