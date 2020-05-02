"""
Score predictions made by language model.
"""
file_name_1 = "Template_1.txt"
file_name_2 = "nouns.txt"
file_name_3 = "singular.txt"
file_name_4 = "plural.txt"

with open(file_name_1) as sentence_file:
	test_sentences_list = sentence_file.read().split("\n")

with open(file_name_2) as nouns_file:
	nouns_list = nouns_file.read().lower().split("\n")

with open(file_name_3) as singular_file:
	singular_list = singular_file.read().lower().split("\n")

with open(file_name_4) as plural_file:
	plural_list = plural_file.read().lower().split("\n")

start_words_singular = ["this", "that"]
start_words_plural = ["these", "those"]

accurate_pred = 0
accurate_sentence = []
complete_list = []

for noun in nouns_list:
	for test_sentence in test_sentences_list:
		words=test_sentence.split(" ")
		words[2] = noun
		complete_test_sentence = " ".join(words)
		complete_list.append(complete_test_sentence)

for complete_sentence in complete_list:
	words = complete_sentence.split(" ")

	if words[0] in start_words_singular:
		if words[2] in singular_list:
			accurate_pred += 1
			accurate_sentence.append(complete_sentence)

	elif words[0] in start_words_plural:
		if words[2] in plural_list:
			accurate_pred += 1
			accurate_sentence.append(complete_sentence)

print("This is the accuracy {}".format(accurate_pred))
print("This is the proportion of correct predictions {}".format(accurate_pred/len(complete_list)))