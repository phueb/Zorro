import random
import inflect

from zorro.words import get_words_for_paradigm
from zorro import configs

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

# todo put templates in list, and loop over them, making sure each can be formatted in teh same way

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'
template3 = '{} {} {} did not happen .'
template4 = 'i saw {} {} {} .'

plural = inflect.engine()

paradigm = 'agreement_across_1_adjective'

# TODO define templates once everywhere

templates = [
        'look at this/these _ _',
        'this/these _ _  went there',
        'this/these _ _  left',
        'i saw this/these _ _',
    ]

# used by choose_words_for_inclusion.py  # TODO is this really necessary? infer this from templates
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

    note: all odd numbered sentences are bad and even good.

    """

    demonstratives_singular = ["this", "that"]
    demonstratives_plural = ["these", "those"]

    nouns_s = get_words_for_paradigm(paradigm, tag='NN', num_words_in_sample=NUM_NOUNS)
    nouns_p = [plural.plural(noun_s) for noun_s in nouns_s]
    adjectives = get_words_for_paradigm(paradigm, tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            # random choices
            adj = random.choice(adjectives)
            noun_s, noun_p = random.choice(list(zip(nouns_s, nouns_p)))

            # check
            if noun_p == noun_s:
                continue

            for pn_s in demonstratives_singular:
                yield template1.format(pn_s, adj, noun_p)  # odd numbered line: bad
                yield template1.format(pn_s, adj, noun_s)  # even numbered line: good

                yield template2.format(pn_s, adj, noun_p)
                yield template2.format(pn_s, adj, noun_s)

                yield template3.format(pn_s, adj, noun_p)
                yield template3.format(pn_s, adj, noun_s)

                yield template4.format(pn_s, adj, noun_p)
                yield template4.format(pn_s, adj, noun_s)

            for pn_p in demonstratives_plural:
                yield template1.format(pn_p, adj, noun_s)  # odd numbered line: bad
                yield template1.format(pn_p, adj, noun_p)  # even numbered line: good

                yield template2.format(pn_p, adj, noun_s)
                yield template2.format(pn_p, adj, noun_p)

                yield template3.format(pn_p, adj, noun_s)
                yield template3.format(pn_p, adj, noun_p)

                yield template4.format(pn_p, adj, noun_s)
                yield template4.format(pn_p, adj, noun_p)

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
