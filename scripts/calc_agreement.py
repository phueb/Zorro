"""
this script calculates human-machine agreement using cohen's kappa

"""

from sklearn.metrics import cohen_kappa_score

from babeval.whole_words import get_whole_words, classify_whole_words

nouns = open('../babeval/agreement_across_1_adjective/annotator_2/nouns.txt', 'r').read().split()

nouns_singular_nltk = classify_whole_words(get_whole_words())['nouns_singular']
nouns_singular_ann2 = open('../babeval/agreement_across_RC/annotator_2/nouns_singular.txt', 'r').read().split()

y1 = []
y2 = []
for w in nouns:

    y1i = "-" if w in nouns_singular_nltk else "P"
    y2i = "-" if w in nouns_singular_ann2 else "P"

    y1.append(y1i)
    y2.append(y2i)
    print(f'{w:<16} {y1i} {y2i}')

ck = cohen_kappa_score(y1, y2)
print(ck)