import random
from typing import List, Dict, Tuple
import inflect

from zorro.words import get_legal_words
from zorro import configs

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'where {} the {} go ?'
template2 = 'what {} the {} do ?'
template3 = 'how {} the {} fit in here ?'
template4 = 'how {} the {} become {} ?'
template5 = 'when {} the {} stop working ?'
template6 = 'when {} the {} start ?'

templates = []  # TODO define templates once everywhere

plural = inflect.engine()


def main():
    """
    example:
    "where does the dog go?" vs. "where does the dogs go?"
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    doing_singular = ["does"]
    doing_plural = ["do"]

    def gen_sentences():
        while True:

            # random choices
            adj = random.choice(adjectives)
            noun_s, noun_p = random.choice(nouns_s_and_p)

            for doing_s in doing_singular:

                yield template1.format(doing_s, noun_p)  # bad
                yield template1.format(doing_s, noun_s)  # good

                yield template2.format(doing_s, noun_p)
                yield template2.format(doing_s, noun_s)

                yield template3.format(doing_s, noun_p)
                yield template3.format(doing_s, noun_s)

                yield template4.format(doing_s, noun_p, adj)
                yield template4.format(doing_s, noun_s, adj)

                yield template5.format(doing_s, noun_p)
                yield template5.format(doing_s, noun_s)

                yield template6.format(doing_s, noun_p)
                yield template6.format(doing_s, noun_s)

            for doing_p in doing_plural:
                yield template1.format(doing_p, noun_s)  # bad
                yield template1.format(doing_p, noun_p)   # good

                yield template2.format(doing_p, noun_s)
                yield template2.format(doing_p, noun_p)

                yield template3.format(doing_p, noun_s)
                yield template3.format(doing_p, noun_p)

                yield template4.format(doing_p, noun_s, adj)
                yield template4.format(doing_p, noun_p, adj)

                yield template5.format(doing_p, noun_s)
                yield template5.format(doing_p, noun_p)

                yield template6.format(doing_p, noun_s)
                yield template6.format(doing_p, noun_p)

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
        elif s1[0] == 'what' and s2[0] == 'what':
            template2pairs.setdefault(templates[1], []).append(pair)
        # template 3
        elif s1[-2] == 'here' and s2[-2] == 'here':
            template2pairs.setdefault(templates[2], []).append(pair)
        # template 4
        elif s1[-3] == 'become' and s2[-3] == 'become':
            template2pairs.setdefault(templates[3], []).append(pair)
        # template 5
        elif s1[-2] == 'working' and s2[-2] == 'working':
            template2pairs.setdefault(templates[4], []).append(pair)
        # template 6
        elif s1[-2] == 'start' and s2[-2] == 'start':
            template2pairs.setdefault(templates[5], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
