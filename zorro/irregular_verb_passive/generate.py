import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 20

template1 = '{} {} {} {} was {} by him .'
template2 = '{} {} {} {} was not {} by her .'
template3 = '{} {} {} {} was {} to him .'  # for use with "given"
template4 = '{} {} {} {} was not {} to her .'  # for use with "given"


def main():
    """
    example:
    "maybe the black dog was taken by him ." vs. "maybe the black dog was took by him ."


    a paradigm that uses just adjectives results in use of 2 adjectives ("taken", "broken") only,
    when the vocab size is 8192 - hence, we do not use this paradigm.
    instead, we use the passive construction which allows us to include the verb "given".
    """

    from zorro.irregular_verb_passive.shared import paradigm, determiners
    from zorro.irregular_verb_passive.shared import vds_vns
    from zorro.words import get_words_for_paradigm
    from zorro.vocab import get_vocab_words
    from zorro import configs

    vocab = get_vocab_words()
    modifiers = ['maybe', 'i think', 'we hope that', 'he said that']
    nouns_s = get_words_for_paradigm(paradigm, 'NN', 0, NUM_NOUNS)
    adjectives = get_words_for_paradigm(paradigm, 'JJ', 0, NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            # random choices
            noun = random.choice(nouns_s)
            det = random.choice(determiners)
            adj = random.choice(adjectives)
            mod = random.choice(modifiers)

            # get two contrasting irregular inflected forms.
            # past participle (vn) is always correct
            vd, vn = random.choice(vds_vns)
            if (vn not in vocab or vd not in vocab) or vn == vd:
                continue

            # exceptional case
            if vn == 'given':
                yield template3.format(mod, det, adj, noun, vn)
                yield template3.format(mod, det, adj, noun, vd)

                yield template4.format(mod, det, adj, noun, vn)
                yield template4.format(mod, det, adj, noun, vd)
            else:
                yield template1.format(mod, det, adj, noun, vn)
                yield template1.format(mod, det, adj, noun, vd)

                yield template2.format(mod, det, adj, noun, vn)
                yield template2.format(mod, det, adj, noun, vd)

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
