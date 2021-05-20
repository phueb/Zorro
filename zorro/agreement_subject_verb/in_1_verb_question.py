import random
from typing import List, Dict, Tuple
import inflect

from zorro.words import get_legal_words
from zorro import configs

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'where {} the {} ?'
template2 = 'what {} the {} ?'
template3 = 'what color {} the {} ?'
template4 = '{} the {} not {} ?'
template5 = '{} the {} where it should be ?'
template6 = '{} the {} where they should be ?'
template7 = '{} the {} something you like ?'
template8 = '{} the {} a good idea ?'

templates = []  # TODO define templates once everywhere

plural = inflect.engine()


def main():
    """
    example:
    "where is the house?" vs "where is the houses?"
    todo "where is the house?" vs "where are the house?"
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    copulas_singular = ["is", "was"]
    copulas_plural = ["are", "were"]

    def gen_sentences():
        while True:

            # random choices
            noun_s, noun_p = random.choice(nouns_s_and_p)
            adj = random.choice(adjectives)

            for copula_s in copulas_singular:

                yield template1.format(copula_s, noun_p)
                yield template1.format(copula_s, noun_s)

                yield template2.format(copula_s, noun_p)
                yield template2.format(copula_s, noun_s)

                yield template3.format(copula_s, noun_p)
                yield template3.format(copula_s, noun_s)

                yield template4.format(copula_s, noun_p, adj)
                yield template4.format(copula_s, noun_s, adj)

                yield template5.format(copula_s, noun_p)
                yield template5.format(copula_s, noun_s)

                # skip template 6 because it is specific to plural copula

                yield template7.format(copula_s, noun_p)
                yield template7.format(copula_s, noun_s)

                yield template8.format(copula_s, noun_p)
                yield template8.format(copula_s, noun_s)

            for copula_p in copulas_plural:

                yield template1.format(copula_p, noun_s)
                yield template1.format(copula_p, noun_p)

                yield template2.format(copula_p, noun_s)
                yield template2.format(copula_p, noun_p)

                yield template3.format(copula_p, noun_s)
                yield template3.format(copula_p, noun_p)

                yield template4.format(copula_p, noun_s, adj)
                yield template4.format(copula_p, noun_p, adj)

                # skip template 5 because it is specific to singular copula

                yield template6.format(copula_p, noun_s)
                yield template6.format(copula_p, noun_p)

                yield template7.format(copula_p, noun_s)
                yield template7.format(copula_p, noun_p)

                yield template8.format(copula_p, noun_s)
                yield template8.format(copula_p, noun_p)

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
        if s1[0] == 'where' and s2[0] == 'where':
            template2pairs.setdefault(templates[0], []).append(pair)
        # template 2
        elif s1[0] == 'what' and s2[0] == 'what' and s1[2] == 'the' and s2[2] == 'the':
            template2pairs.setdefault(templates[1], []).append(pair)
        # template 3
        elif s1[0] == 'what' and s2[0] == 'what' and s1[1] == 'color' and s2[1] == 'color':
            template2pairs.setdefault(templates[2], []).append(pair)
        # template 4
        elif s1[1] == 'the' and s2[1] == 'the' and s1[3] == 'not' and s2[3] == 'not':
            template2pairs.setdefault(templates[3], []).append(pair)
        # template 5
        elif s1[1] == 'the' and s2[1] == 'the' and s1[4] == 'it' and s2[4] == 'it':
            template2pairs.setdefault(templates[4], []).append(pair)
        # template 6
        elif s1[1] == 'the' and s2[1] == 'the' and s1[4] == 'they' and s2[4] == 'they':
            template2pairs.setdefault(templates[5], []).append(pair)
        # template 7
        elif s1[-2] == 'imagined' and s2[-2] == 'imagined':
            template2pairs.setdefault(templates[6], []).append(pair)
        # template 8
        elif s1[-2] == 'idea' and s2[-2] == 'idea':
            template2pairs.setdefault(templates[7], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs

if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
