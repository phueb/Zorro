from collections import Counter
import nltk

#open and read file
with open('childes-20191206_mlm.txt') as f:
    text_string = f.read()
    word = text_string.split()
counter = Counter(word)
most_occur = counter.most_common(4096)
just_word = [x[0] for x in most_occur]

#get pos-tags of all words
list_of_strings = " ".join(just_word)
text = nltk.word_tokenize(list_of_strings)
POS_list = nltk.pos_tag(text)

#separate singular and plural nouns
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma
def merge(list1, list2): 
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

with open(input_directory + file_name_1) as f:
    words_list = f.read().split("\n")
    word_list = []
    isp_list = []
    for word in words_list:
        isp, lemma = isplural(word)
        word_list.append(word)
        isp_list.append(isp)
    merge_list = merge(words_list,isp_list)
    all_plural = [i[0] for i in merge_list if i[1] is False]
    all_singular = [i[0] for i in merge_list if i[1] is True]
