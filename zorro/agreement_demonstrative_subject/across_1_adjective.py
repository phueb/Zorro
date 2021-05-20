import random
from typing import List, Dict, Tuple
import inflect

from zorro.words import get_legal_words
from zorro import configs

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

# todo put templates in list, and loop over them, making sure each can be formatted in teh same way

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'
template3 = '{} {} {} did not happen .'
template4 = 'i saw {} {} {} .'

plural = inflect.engine()

paradigm = 'across_1_adjective'

templates = []  # TODO define templates once everywhere


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    "this green house went there ." vs. "this green houses went there."

    note: all odd numbered sentences are bad and even good.

    """

    demonstratives_singular = ["this", "that"]
    demonstratives_plural = ["these", "those"]

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            # random choices
            adj = random.choice(adjectives)
            noun_s, noun_p = random.choice(nouns_s_and_p)

            for dem_s in demonstratives_singular:
                yield template1.format(dem_s, adj, noun_p)  # odd numbered line: bad
                yield template1.format(dem_s, adj, noun_s)  # even numbered line: good

                yield template2.format(dem_s, adj, noun_p)
                yield template2.format(dem_s, adj, noun_s)

                yield template3.format(dem_s, adj, noun_p)
                yield template3.format(dem_s, adj, noun_s)

                yield template4.format(dem_s, adj, noun_p)
                yield template4.format(dem_s, adj, noun_s)

            for dem_p in demonstratives_plural:
                yield template1.format(dem_p, adj, noun_s)  # odd numbered line: bad
                yield template1.format(dem_p, adj, noun_p)  # even numbered line: good

                yield template2.format(dem_p, adj, noun_s)
                yield template2.format(dem_p, adj, noun_p)

                yield template3.format(dem_p, adj, noun_s)
                yield template3.format(dem_p, adj, noun_p)

                yield template4.format(dem_p, adj, noun_s)
                yield template4.format(dem_p, adj, noun_p)

    # only collect unique sentences
    sentences = set()
    gen = gen_sentences()
    while len(sentences) // 2 < configs.Data.num_pairs_per_paradigm:
        sentence = next(gen)
        if sentence not in sentences:
            yield sentence
        sentences.add(sentence)


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        # template 1
        if s1[0] == 'look' and s2[0] == 'look':
            template2pairs.setdefault(templates[0], []).append(pair)
        # template 2
        elif s1[-2] == 'there' and s2[-2] == 'there':
            template2pairs.setdefault(templates[1], []).append(pair)
        # template 3
        elif s1[-2] == 'here' and s2[-2] == 'here':
            template2pairs.setdefault(templates[2], []).append(pair)
        # template 4
        elif s1[1] == 'saw' and s2[1] == 'saw':
            template2pairs.setdefault(templates[3], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
