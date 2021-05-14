import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

template1 = 'look at {} {} {} {} .'
template2 = '{} {} {} {} went there .'

rules = {
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('this', '{}', '_', '_'),
        template2.format('this', '{}', '_', '_'),
    ],
    ('JJ', 1, NUM_ADJECTIVES): [
        template1.format('this', '_', '{}', '_'),
        template2.format('this', '_', '{}', '_'),
    ],
    ('NN', 0, NUM_NOUNS): [
        template1.format('this', '_', '_', '{}'),
        template2.format('this', '_', '_', '{}'),
    ],
}


def main():
    """
    example:
    "look at this green red house ." vs. "look at this green red houses ."
    "this green red house went there ." vs. "this green red houses went there."
    """

    from zorro.words import get_words_for_paradigm
    from zorro.agreement_across_2_adjectives.shared import paradigm, demonstratives_singular, demonstratives_plural, plural
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    adjectives = get_words_for_paradigm(paradigm, tag='JJ', num_words_in_sample=NUM_ADJECTIVES)
    nouns_s = get_words_for_paradigm(paradigm, tag='NN', num_words_in_sample=NUM_NOUNS)

    def gen_sentences():
        while True:

            noun_s = random.choice(nouns_s)
            noun_p = plural.plural(noun_s)
            if noun_p not in noun_plurals or noun_p == noun_s:
                continue

            # random choices
            demonstrative = random.choice(demonstratives_singular + demonstratives_plural)
            adj1 = random.choice(adjectives)
            adj2 = random.choice(adjectives)

            yield template1.format(demonstrative, adj1, adj2, noun_s)
            yield template1.format(demonstrative, adj1, adj2, noun_p)

            yield template2.format(demonstrative, adj1, adj2, noun_s)
            yield template2.format(demonstrative, adj1, adj2, noun_p)

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