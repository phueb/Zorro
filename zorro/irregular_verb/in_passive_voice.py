import random
import inflect

from zorro.filter import collect_unique_pairs
from zorro.vocab import get_vocab_words
from zorro.words import get_legal_words

template1 = '{} {} {} {} was {} by him .'
template2 = "{} {} {} {} wasn't {} by her ."
template3 = '{} {} {} {} was {} to him .'  # for use with "given"
template4 = "{} {} {} {} wasn't {} to her ."  # for use with "given"

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
    nouns_s = get_legal_words(tag='NN')
    adjectives = get_legal_words(tag='JJ')

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


if __name__ == '__main__':
    for n, s in enumerate(collect_unique_pairs(main)):
        print(f'{n//2+1:>12,}', s)
