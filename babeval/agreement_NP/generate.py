"""
Generate noun phrases for evaluating number agreement Between a demonstrative and a noun
"""
#open and read file
with open('childes-20191206_mlm.txt') as f:
    text_string = f.read()
    punctuation = ['(', ')', ',', '"', '.','?']
    for p in punctuation:
        text_string = text_string.replace(p,'')
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

with open("nouns.txt") as f:
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

#generate test sentences
with open("adjectives.txt") as f:
    adjectives_words_list = f.read().lower().split("\n")
    list_length = len(adjectives_words_list)
    start_words = ['this', 'these', 'that', 'those']
    template_1_list = []

#generate template_1 test sentences
    for start_word in start_words:
        for adjective in adjectives_words_list:
            masked = "[MASKED]"
            template_1 = start_word + " " + adjective + " " + masked
            template_1_list.append(template_1)

#generate template_2 test sentences
    for start_word in start_words:
        for i in range(list_length):
            for j in range(list_length):
                masked = "[MASKED]"
                template_2 = start_word + " " + adjectives_words_list[i] + " " + adjectives_words_list[j] + " " + masked
                if adjectives_words_list[j] == adjectives_words_list[i]:
                    template_2 = ""
#generate template_3 test sentences
    for start_word in start_words:
        masked = "[MASKED]"
        template_3 = start_word + " " +  masked

# Read in file
file_name_1 = "nouns.txt"
file_name_2 = "prepositions.txt"
file_name_3 = "adjectives.txt"
input_directory = 'word_lists/'

with open(input_directory + file_name_1) as nouns_file:
	nouns_list = nouns_file.read().lower().split("\n")

with open(input_directory + file_name_2) as prepositions_file:
	prepositions_list = prepositions_file.read().lower().split("\n")

with open(input_directory + file_name_3) as adjectives_file:
	adjectives_list = adjectives_file.read().lower().split("\n")

# Generate PP templates
PP_list = []
for preposition in prepositions_list:
	for noun in nouns_list:
		PP = preposition + ' ' + 'the' + ' ' + noun
		PP_list.append(PP)

# Generate Prepositions_Sentences
for noun in nouns_list:
	for PP in PP_list:
		for adjective in adjectives_list:
			Prepositions_Sentences = 'the' + ' ' + noun + ' ' + PP + ' ' + "[MASKED]" + ' ' + adjective
			print(Prepositions_Sentences, file = open("agreement_NP_1.txt","a"))



