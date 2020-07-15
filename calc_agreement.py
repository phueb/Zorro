"""
this script calculates human-machine agreement using cohen's kappa

"""

from sklearn.metrics import cohen_kappa_score

from babeval.vocab import get_vocab, classify_vocab

nouns_annotator2 = open('babeval/agreement_across_adjectives/word_lists/nouns_annotator2.txt', 'r').read().split()

nouns_singular_nltk = classify_vocab(get_vocab())['nouns_singular']
nouns_singular_ann2 = open('babeval/agreement_across_RC/word_lists/nouns_singular_annotator2.txt', 'r').read().split()

y1 = []
y2 = []
for w in nouns_annotator2:

    y1i = "-" if w in nouns_singular_nltk else "P"
    y2i = "-" if w in nouns_singular_ann2 else "P"

    y1.append(y1i)
    y2.append(y2i)
    print(f'{w:<16} {y1i} {y2i}')

ck = cohen_kappa_score(y1, y2)
print(ck)