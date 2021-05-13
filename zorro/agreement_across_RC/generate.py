import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 20

template1a = 'the {} that {} like {} {} .'
template1b = 'the {} that {} likes {} {} .'
template2a = 'the {} that is there {} {} .'
template2b = 'the {} that are there {} {} .'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1a.format('{}', 'i', 'is', '_'),
        template2a.format('{}', 'is', '_'),
    ],

    ('JJ', 0, NUM_ADJECTIVES): [
        template1a.format('_', 'i', 'is', '{}'),
        template2a.format('_', 'is', '{}'),
    ],

}


def main():
    """
    example:
    "the dog that i like is green" vs. "the dogs that i like is green"
    """

    from zorro.agreement_across_RC.shared import paradigm, plural, pronouns_3p, pronouns_1p_2p
    from zorro.agreement_across_RC.shared import copulas_plural, copulas_singular
    from zorro.words import get_words_for_paradigm
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
            copula = random.choice(copulas_singular + copulas_plural)
            adj = random.choice(adjectives)

            # object-relative
            for pronoun_1p_2p in pronouns_1p_2p:
                yield template1a.format(noun_s, pronoun_1p_2p, copula, adj)
                yield template1a.format(noun_p, pronoun_1p_2p, copula, adj)
            for pronoun_3p in pronouns_3p:
                yield template1b.format(noun_s, pronoun_3p, copula, adj)
                yield template1b.format(noun_p, pronoun_3p, copula, adj)

            # subject-relative
            if copula in copulas_singular:
                yield template2a.format(noun_s, copula, adj)
                yield template2a.format(noun_p, copula, adj)
            else:
                yield template2b.format(noun_s, copula, adj)
                yield template2b.format(noun_p, copula, adj)

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
