import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 90

template1 = '{} {} something {} {} .'
template2 = '{} {} {} {} {} .'


def main():
    """
    example:
    "mary bit something green just now ." vs. "mary bitten something green just now ."
    "mary bit a green castle just now ." vs. "mary bitten a green castle just now ."

    """

    from zorro.irregular_verb_transitive.shared import paradigm, determiners, names
    from zorro.irregular_verb_transitive.shared import vbds_vbns_transitive
    from zorro.counterbalance import find_counterbalanced_subset
    from zorro.words import get_words_for_paradigm
    from zorro.vocab import get_vocab_words
    from zorro import configs

    names = find_counterbalanced_subset(names, min_size=10, max_size=len(names))
    vocab = get_vocab_words()
    adjectives = get_words_for_paradigm(paradigm, 'JJ', 0, NUM_ADJECTIVES)
    modifiers = ['while you were gone', 'but nothing happened', 'without us', 'when i was not looking']
    nouns_s = get_words_for_paradigm(paradigm, 'NN', 0, NUM_NOUNS)

    def gen_sentences():
        while True:

            # random choices
            noun = random.choice(nouns_s)
            name = random.choice(names)
            det = random.choice(determiners)
            adj = random.choice(adjectives)
            mod = random.choice(modifiers)

            # get two contrasting irregular inflected forms
            vbd, vbn = random.choice(vbds_vbns_transitive)  # past, past participle
            if (vbd not in vocab or vbn not in vocab) or vbd == vbn:
                continue

            # vbd is correct
            yield template1.format(name, vbd, adj, mod)
            yield template1.format(name, vbn, adj, mod)

            # vbn is correct
            yield template1.format(name, 'had ' + vbd, adj, mod)
            yield template1.format(name, 'had ' + vbn, adj, mod)

            # vbd is correct
            yield template2.format(name, vbd, det, noun, mod)
            yield template2.format(name, vbn, det, noun, mod)

            # vbn is correct
            yield template2.format(name, 'had ' + vbd, det, noun, mod)
            yield template2.format(name, 'had ' + vbn, det, noun, mod)

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
