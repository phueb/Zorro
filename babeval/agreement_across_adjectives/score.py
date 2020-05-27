"""
Score predictions made by language model.
The agreement_across_adjectives task should not just calcualte a single accuracy measure, but calculate 5 measures, each quantifying the proportion of model-predictions that correspond to a particular kind of answer:
1. correct noun number
2. incorrect noun number
3. ambiguous noun number ("sheep", "fish")
4. non-noun
5. [UNK] (this means "unknown", which means the model doesn't want to commit to an answer)
"""
from pathlib import Path

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# ie. "look at these pretty girls" "look at these mean [UNK]"

class Agreement_Across_Adjectives:
	def __init__(self, test_sentence_list, ambiguous_nouns_list, plural_list, singular_list, start_words_plural, start_words_singular):

		self.test_sentence_list = test_sentence_list
		self.ambiguous_nouns_list = ambiguous_nouns_list
		self.plural_list = plural_list
		self.singular_list = singular_list
		self.start_words_plural = start_words_plural
		self.start_words_singular = start_words_singular

		self.UNK_list = None
		self.correct_list = None
		self.incorrect_list = None
		self.ambiguous_list = None
		self.non_noun_list = None

		self.UNK_pred = None
		self.correct_pred = None
		self.incorrect_pred = None
		self.ambiguous_pred = None
		self.non_noun_pred = None

		self.UNK_proportion = None
		self.correct_proportion = None
		self.incorrect_proportion = None
		self.ambiguous_proportion = None
		self.non_noun_proportion = None

	def define_measure(self):
		self.UNK_list = []
		self.correct_list = []
		self.incorrect_list = []
		self.ambiguous_list =[]
		self.non_noun_list = []

		for sentence in self.test_sentence_list:
			#[UNK] CONDITION
			if sentence.split(' ')[4] == "[UNK]":
				self.UNK_list.append(sentence)

			#Correct Noun Number
			elif sentence.split(' ')[4] in self.plural_list and sentence.split(' ')[2] in self.start_words_plural:
				self.correct_list.append(sentence)

			elif sentence.split(' ')[4] in self.singular_list and sentence.split(' ')[2] in self.start_words_singular:
				self.correct_list.append(sentence)

			#Incorrect Noun Number
			elif sentence.split(' ')[4] in self.plural_list and sentence.split(' ')[2] in self.start_words_singular:
				self.incorrect_list.append(sentence)

			elif sentence.split(' ')[4] in self.singular_list and sentence.split(' ')[2] in self.start_words_plural:
				self.incorrect_list.append(sentence)

			#Ambiguous Noun
			elif sentence.split(' ')[4] in self.ambiguous_nouns_list:
				self.ambiguous_list.append(sentence)

			#Non_Noun
			else:
				self.non_noun_list.append(sentence)

	def calculate_proportion(self):
		total_sentence = len(self.test_sentence_list)

		self.UNK_pred = len(self.UNK_list)
		self.correct_pred = len(self.correct_list)
		self.incorrect_pred = len(self.incorrect_list)
		self.ambiguous_pred = len(self.ambiguous_list)
		self.non_noun_pred = len(self.non_noun_list)

		self.UNK_proportion = self.UNK_pred / total_sentence 
		self.correct_proportion = self.correct_pred / total_sentence 
		self.incorrect_proportion = self.incorrect_pred / total_sentence 
		self.ambiguous_proportion = self.ambiguous_pred / total_sentence
		self.non_noun_proportion = self.non_noun_pred / total_sentence

	def visualize_proportion(self):
		objects = ("correct noun", "incorrect noun", "ambiguous noun", "non-noun", "[UNK]")
		y_pos = np.arange(len(objects))
		y_bar = [self.correct_proportion, self.incorrect_proportion, self.ambiguous_proportion, self.non_noun_proportion, self.UNK_proportion]

		plt.bar(y_pos, y_bar, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		plt.ylabel('proportion of total predictions that are in the category')
		plt.title('Overview of Five Categories of Agreement_Across_Adjectives')
		mng = plt.get_current_fig_manager()
		mng.full_screen_toggle()
		# plt.savefig('figure1.png', dpi=700)
		plt.show()

	def print_output(self):
		print("correct noun: {}".format(self.correct_proportion))
		print("incorrect noun: {}".format(self.incorrect_proportion))
		print("ambiguous noun: {}".format(self.ambiguous_proportion))
		print("non-noun: {}".format(self.non_noun_proportion))
		print("[UNK]: {}".format(self.UNK_proportion))

def format_BERT_output(sentence_file_name):
	file = open(sentence_file_name, "r")
	lines = file.readlines()
	file.close()

	lst_1 = []
	for line in lines:
		parts = line.split()
		if len(parts) == 2:
			lst_1.append(parts)

	lst_2 = []
	for i in lst_1:
		lst_2.append(i[0])

	n = 6
	test_sentence_list = []
	x = [lst_2[i:i + n] for i in range(0, len(lst_2), n)]
	for i in x:
		x = " ".join(i)
		test_sentence_list.append(x)

	return test_sentence_list


def main(sentence_file_name):
	data_folder_1 = Path("../../word_lists/4096")
	file_name_1 = data_folder_1 / 'nouns.txt'
	file_name_2 = data_folder_1 / 'nouns_singular_annotator1.txt'
	file_name_3 = data_folder_1 / 'nouns_plural_annotator1.txt'
	file_name_4 = data_folder_1 / 'nouns_ambiguous_number_annotator1.txt'
	
	# for Test_Sentence

	with open(file_name_1) as nouns_file:
		nouns_list = nouns_file.read().split("\n")

	with open(file_name_2) as singular_file:
		singular_list = singular_file.read().split("\n")

	with open(file_name_3) as plural_file:
		plural_list = plural_file.read().split("\n")

	# for Agreement_Across_Adjectives:
	with open(file_name_4) as ambiguous_nouns:
		ambiguous_nouns_list = ambiguous_nouns.read().split("\n")

	test_sentence_list = format_BERT_output(sentence_file_name)

	# separate start words
	start_words_singular = ["this", "that"]
	start_words_plural = ["these", "those"]
	start_words = start_words_singular + start_words_plural
	prep_verbs = ["is", "are"]
	verbs = ["does", "do"]

	# Counting number agreements for agreement_across_adjectives:
	agreement_across_adj = Agreement_Across_Adjectives(test_sentence_list, ambiguous_nouns_list, plural_list, singular_list, start_words_plural, start_words_singular)
	agreement_across_adj.define_measure()
	agreement_across_adj.calculate_proportion()
	agreement_across_adj.visualize_proportion()
	agreement_across_adj.print_output()

main("probing_dummy_results_17000.txt")  # enter the BERT ouput file here to score accuracy



