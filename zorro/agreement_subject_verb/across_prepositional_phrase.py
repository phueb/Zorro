import random
from typing import List, Dict, Tuple
import inflect

from zorro.words import get_legal_words
from zorro import configs

NUM_NOUNS = 50
NUM_ADJECTIVES = 50

template1 = 'the {} on the {} {} {} .'
template2 = 'the {} by the {} {} {} .'

templates = []  # TODO define templates once everywhere

plural = inflect.engine()


def main():
    """
    example:
    "the dog on the mats is brown" vs "the dog on the mats are brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of sentences containing plural vs. singular object nouns
    2. subject with object number is counterbalanced such that:
        -singular subjects occur with 50:50 singular:plural objects
        -plural   subjects occur with 50:50 singular:plural objects
    """

    nouns_s_and_p = [(noun_s, plural.plural(noun_s))
                     for noun_s in get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
                     if plural.plural(noun_s) != noun_s]
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    copulas_singular = ["is", "was"]
    copulas_plural = ["are", "were"]

    def gen_sentences():

        while True:

            # counter-balance singular vs plural with subj vs. obj
            sub_s, sub_p = random.choice(nouns_s_and_p)
            obj_s, obj_p = random.choice(nouns_s_and_p)

            # random choices
            template = random.choice([template1, template2])
            adj = random.choice(adjectives)

            for copula_s in copulas_singular:
                # contrast is in number agreement between subject and copula
                yield template.format(sub_p, obj_s, copula_s, adj)  # bad
                yield template.format(sub_s, obj_s, copula_s, adj)  # good

                # same as above, except that object number is opposite
                yield template.format(sub_p, obj_p, copula_s, adj)
                yield template.format(sub_s, obj_p, copula_s, adj)

            for copula_p in copulas_plural:
                # contrast is in number agreement between subject and copula
                yield template.format(sub_s, obj_s, copula_p, adj)  # bad
                yield template.format(sub_p, obj_s, copula_p, adj)  # good

                # same as above, except that object number is opposite
                yield template.format(sub_s, obj_p, copula_p, adj)
                yield template.format(sub_p, obj_p, copula_p, adj)

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
        if s1[2] == 'on' and s2[2] == 'on':
            template2pairs.setdefault(templates[0], []).append(pair)
        # template 2
        elif s1[2] == 'by' and s2[2] == 'by':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
