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

import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# ie. "look at these pretty girls" "look at these mean [UNK]"

class Agreement_Across_Adjectives:
	def __init__(self, test_sentence_list, ambiguous_nouns_list, plural_list, singular_list, start_words_plural,
				 start_words_singular):

		self.test_sentence_list = test_sentence_list
		self.ambiguous_nouns_list = ambiguous_nouns_list
		self.plural_list = plural_list
		self.singular_list = singular_list + ['[NAME]', 'one']
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
		self.ambiguous_list = []
		self.non_noun_list = []

		for sentence in self.test_sentence_list:
			# sentence is a list

			print(sentence)
			predicted_noun = sentence[-2]  # TODO get index by checking where [MASK] is in input sentence
			start_word = [w for w in sentence if w in self.start_words_plural + self.start_words_singular][0]

			print(predicted_noun)

			assert start_word in self.start_words_plural + self.start_words_singular

			# [UNK] CONDITION
			if predicted_noun == "[UNK]":
				self.UNK_list.append(sentence)

			# Correct Noun Number
			elif predicted_noun in self.plural_list and start_word in self.start_words_plural:
				self.correct_list.append(sentence)

			elif predicted_noun in self.singular_list and start_word in self.start_words_singular:
				self.correct_list.append(sentence)

			# Incorrect Noun Number
			elif predicted_noun in self.plural_list and start_word in self.start_words_singular:
				self.incorrect_list.append(sentence)

			elif predicted_noun in self.singular_list and start_word in self.start_words_plural:
				self.incorrect_list.append(sentence)

			# Ambiguous Noun
			elif predicted_noun in self.ambiguous_nouns_list:
				self.ambiguous_list.append(sentence)

			# Non_Noun
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

	def visualize_proportion(self, sentence_file_name):
		objects = ("correct\nnoun", "incorrect\nnoun", "ambiguous\nnoun", "non-noun", "[UNK]")
		y_pos = np.arange(len(objects))
		y_bar = [self.correct_proportion, self.incorrect_proportion, self.ambiguous_proportion,
				 self.non_noun_proportion, self.UNK_proportion]

		plt.bar(y_pos, y_bar, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		plt.ylabel('proportion of total predictions that are in the category')
		plt.title(f'Agreement_Across_Adjectives\nn={len(self.test_sentence_list)}\n{sentence_file_name}')
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

	col2 = []
	for line in lines:
		parts = line.split()
		if len(parts) == 2:
			col2.append(parts[-1])

	test_sentence_list = [[]]
	for w in col2:
		test_sentence_list[-1].append(w)
		if w == '.':
			test_sentence_list.append([])

	if not test_sentence_list[-1]:
		del test_sentence_list[-1]

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
	agreement_across_adj = Agreement_Across_Adjectives(test_sentence_list, ambiguous_nouns_list, plural_list,
													   singular_list, start_words_plural, start_words_singular)
	agreement_across_adj.define_measure()
	agreement_across_adj.calculate_proportion()
	agreement_across_adj.visualize_proportion(sentence_file_name)
	agreement_across_adj.print_output()


main("probing_dummy_results_79000.txt")  # enter the BERT ouput file here to score accuracy
