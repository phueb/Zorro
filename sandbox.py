"""
this script is used as a general workspace for loading or saving files, inspecting their contents, etc.

"""


from babeval.vocab import get_vocab, classify_vocab, save_to_txt




nouns_annotator2 = open('babeval/agreement_across_adjectives/nouns_annotator2.txt', 'r').read().split()

nouns_singular_ann2 = open('babeval/agreement_across_adjectives/nouns_singular_annotator2.txt', 'r').read().split()
nouns_ambiguou_ann2 = open('babeval/agreement_across_adjectives/nouns_ambiguous_number_annotator2.txt', 'r').read().split()

plurals = [w for w in nouns_annotator2 if w not in nouns_singular_ann2 and w not in nouns_ambiguou_ann2]
save_to_txt(plurals, file_name='nouns_plural_annotator2.txt')




