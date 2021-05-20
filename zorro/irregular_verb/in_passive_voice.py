import random
from typing import List, Dict, Tuple
import inflect

from zorro.vocab import get_vocab_words
from zorro.words import get_legal_words
from zorro import configs

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

template1 = '{} {} {} {} was {} by him .'
template2 = '{} {} {} {} was not {} by her .'
template3 = '{} {} {} {} was {} to him .'  # for use with "given"
template4 = '{} {} {} {} was not {} to her .'  # for use with "given"

templates = []  # TODO define templates once everywhere

plural = inflect.engine()


def main():
    """
    example:
    "maybe the black dog was taken by him ." vs. "maybe the black dog was took by him ."


    a paradigm that uses just adjectives results in use of 2 adjectives ("taken", "broken") only,
    when the vocab size is 8192 - hence, we do not use this paradigm.
    instead, we use the passive construction which allows us to include the verb "given".
    """

    vocab = get_vocab_words()
    modifiers = ['maybe', 'i think', 'we hope that', 'he said that']
    nouns_s = get_legal_words(tag='NN', num_words_in_sample=NUM_NOUNS)
    adjectives = get_legal_words(tag='JJ', num_words_in_sample=NUM_ADJECTIVES)

    determiners = ['the', 'this', 'one', 'your']

    vds_vns = [
        ('wore', 'worn'),
        ('broke', 'broken'),
        ('hid', 'hidden'),
        ('forgot', 'forgotten'),
        ('took', 'taken'),

        ('ate', 'eaten'),
        ('drank', 'drunk'),
        ('saw', 'seen'),
        ('chose', 'chosen'),
        ('threw', 'thrown'),
        ('beat', 'beaten'),

        # ditransitive
        ('forbade', 'forbidden'),
        ('gave', 'given'),
    ]

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
                yield template3.format(mod, det, adj, noun, vd)  # bad
                yield template3.format(mod, det, adj, noun, vn)  # good

                yield template4.format(mod, det, adj, noun, vd)
                yield template4.format(mod, det, adj, noun, vn)
            else:
                yield template1.format(mod, det, adj, noun, vd)
                yield template1.format(mod, det, adj, noun, vn)

                yield template2.format(mod, det, adj, noun, vd)
                yield template2.format(mod, det, adj, noun, vn)

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
        if s1[-1] == '.':
            template2pairs.setdefault(templates[0], []).append(pair)

        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
