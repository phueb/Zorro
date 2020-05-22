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
		plt.title('overview of five categories of agreement_across_adjectives')
		# plt.savefig('figure1.png', dpi=700)
		plt.show()

class Test_Sentence:
	def __init__(self, test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
				 start_words_plural, start_words, prep_verbs, verbs):

		# put pre-assigned word lists into the Test_Sentence class

		self.test_sentence_list = test_sentence_list
		self.nouns_list = nouns_list
		self.singular_list = singular_list
		self.plural_list = plural_list
		self.start_words_singular = start_words_singular
		self.start_words_plural = start_words_plural
		self.start_words = start_words
		self.prep_verbs = prep_verbs
		self.verbs = verbs

		#categorize sentences based on different sentence structures

		self.template_1_list = None
		self.template_2_list = None
		self.template_3_list = None
		self.template_prep = None
		self.template_RC = None
		self.template_question_1 = None
		self.template_question_2 = None

		#complete each sentence by replacing [MASK] with word from respective word list

		self.sentence_1_complete = None
		self.sentence_2_complete = None
		self.sentence_3_complete = None
		self.prep_complete = None
		self.RC_complete = None
		self.question_1_complete = None
		self.question_2_complete = None

		#count accuracy for number agreements

		self.accurate_pred_1 = None
		self.accurate_pred_2 = None
		self.accurate_pred_3 = None
		self.accurate_pred_prep = None
		self.accurate_pred_RC = None
		self.accurate_pred_question_1 = None
		self.accurate_pred_question_2 = None

		#store accurate sentences in list

		self.accurate_sentence_1 = None
		self.accurate_sentence_2 = None
		self.accurate_sentence_3 = None
		self.accurate_sentence_prep = None
		self.accurate_sentence_RC = None
		self.accurate_sentence_question = None

		#calculate total sentences for template 1 & 2 ; preparing for calculating accuracy

		self.total_test_sentence_1_2 = None
		self.total_question = None

		#get accuracy (when a file contains multiple sentence structures)

		self.accuracy_adj  = None
		self.accuracy_question = None
		
		#get proportion

		self.proportion_adj = None
		self.proportion_prep = None
		self.proportion_RC = None
		self.proportion_question = None

	def differentiate_templates(self):
		self.template_1_list = []
		self.template_2_list = []
		self.template_3_list = []
		self.template_prep = []
		self.template_RC = []
		self.template_question_1 = []
		self.template_question_2 = []

		for test_sentence in self.test_sentence_list:

			# agreement_across_adjectives/template_1
			if len(test_sentence.split(' ')) == 4:
				template_1_sentence = test_sentence
				self.template_1_list.append(template_1_sentence)

			# agreement_across_adjectives/template_2
			elif len(test_sentence.split(' ')) == 5 and test_sentence.split(' ')[0] in self.start_words:
				template_2_sentence = test_sentence
				self.template_2_list.append(template_2_sentence)

			# agreement_across_adjectives/template_3
			elif len(test_sentence.split(' ')) == 3:
				template_3_sentence = test_sentence
				self.template_3_list.append(template_3_sentence)

			# agreement_across_PP
			elif len(test_sentence.split(' ')) == 8 and test_sentence.split(' ')[3] == "the":
				template_prep_sentence = test_sentence
				self.template_prep.append(template_prep_sentence)

			# agreement_across_RC
			elif len(test_sentence.split(' ')) == 8 and test_sentence.split(' ')[2] == "that":
				template_RC = test_sentence
				self.template_RC.append(template_RC)

			# agreement_in_question_1
			elif len(test_sentence.split(' ')) == 5 and test_sentence.split(' ')[0] == "where":
				template_question_1 = test_sentence
				self.template_question_1.append(template_question_1)

			# agreement_in_question_2
			else:
				template_question_2 = test_sentence
				self.template_question_2.append(template_question_2)

	def replace_mask_for_template_1(self):
		self.sentence_1_complete = []
		for noun in self.nouns_list:
			for sentence_1 in self.template_1_list:
				words = sentence_1.split(" ")
				words[2] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_1_complete.append(complete_test_sentence)

	def replace_mask_for_template_2(self):
		self.sentence_2_complete = []
		for noun in self.nouns_list:
			for sentence_2 in self.template_2_list:
				words = sentence_2.split(" ")
				words[3] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_2_complete.append(complete_test_sentence)

	def replace_mask_for_template_3(self):
		self.sentence_3_complete = []
		for noun in self.nouns_list:
			for sentence_3 in self.template_3_list:
				words = sentence_3.split(" ")
				words[1] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_3_complete.append(complete_test_sentence)

	def replace_mask_for_template_prep(self):
		self.prep_complete = []
		for verb in self.prep_verbs:
			for prep_sentence in self.template_prep:
				words = prep_sentence.split(" ")
				words[5] = verb
				complete_test_sentence = " ".join(words)
				self.prep_complete.append(complete_test_sentence)

	def replace_mask_for_template_RC(self):
		self.RC_complete = []
		for verb in self.prep_verbs:
			for sentence in self.template_RC:
				words = sentence.split(" ")
				words[5] = verb
				complete_test_sentence = " ".join(words)
				self.RC_complete.append(complete_test_sentence)

	def replace_mask_for_template_question(self):
		self.question_1_complete = []
		self.question_2_complete = []

		# question_1 

		for prep_verb in self.prep_verbs:
			for question in self.template_question_1:
				words = question.split(" ")
				words[1] = prep_verb
				complete_test_sentence = " ".join(words)
				self.question_1_complete.append(complete_test_sentence)

		# question_2

		for verb in self.verbs:
			for question in self.template_question_2:
				words = question.split(" ")
				words[1] = verb
				complete_test_sentence = " ".join(words)
				self.question_2_complete.append(complete_test_sentence)

	def count_template_1_accuracy(self):
		self.accurate_pred_1 = 0
		self.accurate_sentence_1 = []

		for complete_sentence in self.sentence_1_complete:
			words = complete_sentence.split(" ")
			if words[0] in self.start_words_singular:
				if words[2] in self.singular_list:
					self.accurate_pred_1 += 1
					self.accurate_sentence_1.append(complete_sentence)

			elif words[0] in self.start_words_plural:
				if words[2] in self.plural_list:
					self.accurate_pred_1 += 1
					self.accurate_sentence_1.append(complete_sentence)


	def count_template_2_accuracy(self):
		self.accurate_pred_2 = 0
		self.accurate_sentence_2 = []

		for complete_sentence in self.sentence_2_complete:
			words = complete_sentence.split(" ")
			if words[0] in self.start_words_singular:
				if words[3] in self.singular_list:
					self.accurate_pred_2 += 1
					self.accurate_sentence_2.append(complete_sentence)
			elif words[0] in self.start_words_plural:
				if words[3] in self.plural_list:
					self.accurate_pred_2 += 1
					self.accurate_sentence_2.append(complete_sentence)

	def count_template_3_accuracy(self):
		self.accurate_pred_3 = 0
		self.accurate_sentence_3 = []

		for complete_sentence in self.sentence_3_complete:
			words = complete_sentence.split(" ")
			if words[0] in self.start_words_singular:
				if words[1] in self.singular_list:
					self.accurate_pred_3 += 1
					self.accurate_sentence_3.append(complete_sentence)

			elif words[0] in self.start_words_plural:
				if words[1] in self.plural_list:
					self.accurate_pred_3 += 1
					self.accurate_sentence_3.append(complete_sentence)

	def count_prep_accuracy(self):
		self.accurate_pred_prep = 0
		self.accurate_sentence_prep = []

		for complete_sentence in self.prep_complete:
			words = complete_sentence.split(" ")
			if words[5] == self.prep_verbs[0]:
				if words[1] in self.singular_list:
					self.accurate_pred_prep += 1
					self.accurate_sentence_prep.append(complete_sentence)

			elif words[5] == self.prep_verbs[1]:
				if words[1] in self.plural_list:
					self.accurate_pred_prep += 1
					self.accurate_sentence_prep.append(complete_sentence)

	def count_RC_accuracy(self):
		self.accurate_pred_RC = 0
		self.accurate_sentence_RC = []

		for complete_sentence in self.RC_complete:
			words = complete_sentence.split(" ")
			if words[5] == self.prep_verbs[0]:
				if words[1] in self.singular_list:
					self.accurate_pred_RC += 1
					self.accurate_sentence_RC.append(complete_sentence)

			elif words[5] == self.prep_verbs[1]:
				if words[1] in self.plural_list:
					self.accurate_pred_RC += 1
					self.accurate_sentence_RC.append(complete_sentence)

	def count_question_accuracy(self):
		self.accurate_pred_question_1 = 0
		self.accurate_pred_question_2 = 0
		self.accurate_sentence_question = []

		for complete_sentence in self.question_1_complete:
			words = complete_sentence.split(" ")
			if words[1] == self.prep_verbs[0]:
				if words[3] in self.singular_list:
					self.accurate_pred_question_1 += 1
					self.accurate_sentence_question.append(complete_sentence)

			elif words[1] == self.prep_verbs[1]:
				if words[3] in self.plural_list:
					self.accurate_pred_question_1 += 1
					self.accurate_sentence_question.append(complete_sentence)

		for complete_sentence in self.question_2_complete:
			words = complete_sentence.split(" ")
			if words[1] == self.verbs[0]:
				if words[3] in self.singular_list:
					self.accurate_pred_question_2 += 1
					self.accurate_sentence_question.append(complete_sentence)

			elif words[1] == self.prep_verbs[1]:
				if words[3] in self.plural_list:
					self.accurate_pred_question_2 += 1
					self.accurate_sentence_question.append(complete_sentence)


	def count_accuracy(self):

		self.accuracy_adj = int(self.accurate_pred_1) + int(self.accurate_pred_2) + int(self.accurate_pred_3)
		self.total_test_sentence_adjectives = len(self.sentence_1_complete) + len(self.sentence_2_complete) + len(self.sentence_3_complete)

		self.accuracy_question = int(self.accurate_pred_question_1) + int(self.accurate_pred_question_2)
		self.total_question = len(self.question_1_complete) + len(self.question_2_complete)

	def count_proportion(self):

		try:
			self.proportion_adj = int(self.accuracy_adj) / self.total_test_sentence_adjectives
			self.proportion_prep = int(self.accurate_pred_prep) / len(self.prep_complete)
			self.proportion_RC = int(self.accurate_pred_RC) / len(self.RC_complete)

		except ZeroDivisionError:
			self.proportion_adj = 0
			self.proportion_prep = 0
			self.proportion_RC = 0

		try:
			self.proportion_question = int(self.accuracy_question) / self.total_question
		except ZeroDivisionError:
			self.proportion_question = 0


	def print_output(self):
		print("Accuracy (agreement_across_adjectives) : {}".format(self.accuracy_adj))
		print("Proportion of correct predictions (agreement_across_adjectives) : {}".format(self.proportion_adj))

		print("Accuracy (agreement_across_PP): {}".format(self.accurate_pred_prep))
		print("Proportion of correct predictions (agreement_across_PP): {}".format(self.proportion_prep))

		print("Accuracy (agreement_across_RC): {}".format(self.accurate_pred_RC))
		print("Proportion of correct predictions (agreement_across_RC): {}".format(self.proportion_RC))

		print("Accuracy (agreement_in_question): {}".format(self.accuracy_question))
		print("Proportion of correct predictions (agreement_in_question): {}".format(self.proportion_question))


def main(sentence_file_name):
	data_folder_1 = Path("/Users/vivianyu/Desktop/Babeval-master/output")
	data_folder_2 = Path("/Users/vivianyu/Desktop/Babeval-master/word_lists")
	file_name_1 = data_folder_1 / sentence_file_name # this should be one of the file from the output folder
	file_name_2 = data_folder_2 / 'nouns.txt'
	file_name_3 = data_folder_2 / 'singulars.txt'
	file_name_4 = data_folder_2 / 'plurals.txt'

	file_name_5 = data_folder_2 / 'ambiguous_nouns.txt'

	# open and read files

	# for Test_Sentence
	with open(file_name_1) as sentence_file:
		test_sentence_list = sentence_file.read().split("\n")

	with open(file_name_2) as nouns_file:
		nouns_list = nouns_file.read().lower().split("\n")

	with open(file_name_3) as singular_file:
		singular_list = singular_file.read().lower().split("\n")

	with open(file_name_4) as plural_file:
		plural_list = plural_file.read().lower().split("\n")

	# for Agreement_Across_Adjectives:
	with open(file_name_5) as ambiguous_nouns:
		ambiguous_nouns_list = ambiguous_nouns.read().lower().split("\n")

	# separate start words
	start_words_singular = ["this", "that"]
	start_words_plural = ["these", "those"]
	start_words = start_words_singular + start_words_plural
	prep_verbs = ["is", "are"]
	verbs = ["does", "do"]

	#Counting number agreements for agreement_across_adjectives:
	agreement_across_adj = Agreement_Across_Adjectives(test_sentence_list, ambiguous_nouns_list, plural_list, singular_list, start_words_plural, start_words_singular)
	agreement_across_adj.define_measure()
	agreement_across_adj.calculate_proportion()
	agreement_across_adj.visualize_proportion()


	#Counting number agreements based on single/plural word_lists

	# test_sentence = Test_Sentence(test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
	# 							  start_words_plural, start_words, prep_verbs, verbs)

	# test_sentence.differentiate_templates()

	# test_sentence.replace_mask_for_template_1()
	# test_sentence.replace_mask_for_template_2()
	# test_sentence.replace_mask_for_template_3()
	# test_sentence.replace_mask_for_template_prep()
	# test_sentence.replace_mask_for_template_RC()
	# test_sentence.replace_mask_for_template_question()

	# test_sentence.count_template_1_accuracy()
	# test_sentence.count_template_2_accuracy()
	# test_sentence.count_template_3_accuracy()
	# test_sentence.count_prep_accuracy()
	# test_sentence.count_RC_accuracy()
	# test_sentence.count_question_accuracy()

	# test_sentence.count_accuracy()
	# test_sentence.count_proportion()
	# test_sentence.print_output()


main(sentence_file_name = "dummy_file.txt")  # enter one of the text_file name from output folder in .txt form here



