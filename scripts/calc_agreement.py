"""
this script calculates human-machine agreement using cohen's kappa

"""

from sklearn.metrics import cohen_kappa_score

from zorro.vocab import get_vocab_words

WW_NAME = 'c-w-n'
PATH1 = None
PATH2 = None

nouns = get_vocab_words(WW_NAME, 'NN') + get_vocab_words(WW_NAME, 'NNS')

nouns_singular_ann1 = open(PATH1, 'r').read().split()
nouns_singular_ann2 = open(PATH2, 'r').read().split()

y1 = []
y2 = []
for w in nouns:

    y1i = "-" if w in nouns_singular_ann1 else "P"
    y2i = "-" if w in nouns_singular_ann2 else "P"

    y1.append(y1i)
    y2.append(y2i)
    print(f'{w:<16} {y1i} {y2i}')

ck = cohen_kappa_score(y1, y2)
print(ck)