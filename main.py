
import sys
sys.path.insert(1, 'babeval/agreement_NP/')
import generate

file_name_1 = "nouns.txt"
file_name_2 = "adjectives.txt"
file_name_3 = "prepositions.txt"
file_name_4 = "pronouns.txt"
file_name_5 = "pronoun_third_person.txt"
input_directory = "word_lists/"

start_words = ['this', 'these', 'that', 'those']
mask = "[MASK]"

#open and read word_lists
with open(input_directory + file_name_1) as f:
    nouns_list = f.read().lower().split("\n")

with open(input_directory + file_name_2) as f:
    adjectives_list = f.read().lower().split("\n")

with open(input_directory + file_name_3) as f:
    prepositions_list = f.read().lower().split("\n")

with open(input_directory + file_name_4) as f:
    pronouns_list = f.read().lower().split("\n")

with open(input_directory + file_name_5) as f:
    pronouns_third_person_list = f.read().lower().split("\n")

generate.get_agreement_across_adjectives(start_words, adjectives_list)
generate.get_agreement_across_PP(prepositions_list, nouns_list, adjectives_list)
generate.get_agreement_across_RC(nouns_list, pronouns_list, adjectives_list, pronouns_third_person_list)

# To randomly select test_sentences to print out:

# with open(file_name) as f:
# 	f_lst = f.read().split("\n")

# rng = default_rng()
# numbers = rng.choice(len(f_lst), size=2500, replace=False)

# for i in numbers:
# 	print(f_lst[i], file = open("file_name","a"))
