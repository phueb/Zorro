# find 4096 most frequent words from the master_word_list

from collections import Counter
import nltk
import os
from pathlib import Path
import os.path

# cwd = os.getcwd() #get current file_path
# print(cwd)

data_folder = Path("/Users/vivianyu/Desktop/Babeval-master/babeval")
file_to_open = data_folder / "childes-20191206_vocab.txt"

with open(file_to_open) as f:
    text_string_list = []
    text_string = f.read().split()
    text_string_list.append(text_string)
    my_list = [t[1::2] for t in text_string_list]
    for lst in my_list:
        clean_word_list = lst[:4096]
        # for word in clean_word_list:
        #   print(word, file = open("childes-20191206_mlm_4096.txt","a"))

# get pos_tag
list_of_strings = " ".join(clean_word_list)
text = nltk.word_tokenize(list_of_strings)
POS_list = nltk.pos_tag(text)
all_nouns = [token for token in POS_list if token[1] in ['NN','NNS','NNP','NNPS']]
all_verbs = [token for token in POS_list if token[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']]
all_adjectives = [token for token in POS_list if token[1] in ['JJ','JJR','JJS']]

# print(all_nouns)
# print(all_verbs)
# print(all_adjectives)

# separate singular and plural nouns
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma
def merge(list1, list2): 
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

data_folder_1 = Path("/Users/vivianyu/Desktop/Babeval-master/word_lists_master")
file_to_open_1 = data_folder_1 / "nouns.txt"


with open(file_to_open_1) as f:
    words_list = f.read().split("\n")
    word_list = []
    isp_list = []
    for word in words_list:
        isp, lemma = isplural(word)
        word_list.append(word)
        isp_list.append(isp)
    merge_list = merge(words_list,isp_list)
    all_plural = [i[0] for i in merge_list if i[1] is True]
    all_singular = [i[0] for i in merge_list if i[1] is False]
    for word in all_singular:
        print(word, file = open("singulars.txt","a"))
    for word in all_plural:
        print(word, file = open("plurals.txt","a"))


#sort word_lists        
save_path = "/Users/vivianyu/Desktop/Babeval-master/word_lists" 
file_name = "pronoun_third_person.txt" #can be any file from the master word lists
completeName = os.path.join(save_path, file_name) #make file be generated in any assigned folder
file1 = open(completeName, "a")

file_to_open_2 = data_folder_1 / file_name
with open(file_to_open_2) as f:
    f = f.read().split("\n")
    word_list = sorted(f)
    # for word in word_list:
    #     print(word, file = file1) 



