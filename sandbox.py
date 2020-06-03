"""
this script is used as a general workspace for loading or saving files, inspecting their contents, etc.

"""


from babeval.vocab import get_vocab, classify_vocab, save_to_txt


save_to_txt(classify_vocab(get_vocab())['nouns'], file_name='nouns_nltk.txt')


# quick way to load words
nouns_vivianna = open('word_lists/nouns_annotator1.txt', 'r').read().split()

nouns_nltk = open('word_lists/nouns_nltk.txt', 'r').read().split()
# for w in nouns_nltk:
#     print(f'{w:<16} {"Vivianna" if w in nouns_vivianna else ""}')

print()
# print([w for w in nouns_vivianna if w not in nouns_nltk])
# print(len([w for w in nouns_vivianna if w not in nouns_nltk]))
# print([w for w in nouns_vivianna if w not in nouns_nltk and w in get_vocab()])
print(len([w for w in nouns_vivianna if w not in nouns_nltk and w in get_vocab()]))

