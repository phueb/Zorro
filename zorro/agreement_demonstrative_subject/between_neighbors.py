import random
from typing import List, Dict, Tuple
import inflect

from zorro.words import get_legal_words
from zorro import configs

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = '{} {} must be {} .'
template2 = '{} {} can be {} .'

templates = []

plural = inflect.engine()


def main():
    """
    example:
    "look at this house" vs. "look at this houses"

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
            noun_s, noun_p = random.choice(nouns_s_and_p)
            adj = random.choice(adjectives)

            for dem_s in demonstratives_singular:

                yield template1.format(dem_s, noun_p, adj)  # bad
                yield template1.format(dem_s, noun_s, adj)  # good

                yield template2.format(dem_s, noun_p, adj)
                yield template2.format(dem_s, noun_s, adj)

            for dem_p in demonstratives_plural:
                yield template1.format(dem_p, noun_s, adj)  # bad
                yield template1.format(dem_p, noun_p, adj)  # good

                yield template2.format(dem_p, noun_s, adj)
                yield template2.format(dem_p, noun_p, adj)

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
        if s1[2] == 'must' and s2[2] == 'must':
            template2pairs.setdefault(templates[0], []).append(pair)
        elif s1[2] == 'can' and s2[2] == 'can':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
