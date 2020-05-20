"""
Score predictions made by language model.
"""
from pathlib import Path

class Test_Sentence:
	def __init__(self, test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
				 start_words_plural, prep_verbs, verbs):

		# put pre-assigned word lists into the Test_Sentence class

		self.test_sentence_list = test_sentence_list
		self.nouns_list = nouns_list
		self.singular_list = singular_list
		self.plural_list = plural_list
		self.start_words_singular = start_words_singular
		self.start_words_plural = start_words_plural
		self.prep_verbs = prep_verbs
		self.verbs = verbs

		#categorize sentences based on different sentence structures

		self.template_1_list = None
		self.template_2_list = None
		self.template_3_list = None
		self.template_prep = None
		self.template_verb = None

		#complete each sentence by replacing [MASK] with word from respective word list

		self.sentence_1_complete = None
		self.sentence_2_complete = None
		self.sentence_3_complete = None
		self.prep_complete = None
		self.verb_complete = None

		#count accuracy for number agreements

		self.accurate_pred_1 = None
		self.accurate_pred_2 = None
		self.accurate_pred_3 = None
		self.accurate_pred_prep = None
		self.accurate_pred_verb = None

		#store accurate sentences in list

		self.accurate_sentence_1 = None
		self.accurate_sentence_2 = None
		self.accurate_sentence_3 = None
		self.accurate_sentence_prep = None
		self.accurate_sentence_verb = None

		#calculate total sentences for template 1 & 2 ; preparing for calculating accuracy

		self.total_test_sentence_1_2 = None

		#get accuracy and proportion for each sentence file

		self.accuracy_1_2 = None
		self.accuracy_proportion = None
		self.proportion_prep = None
		self.proportion_verb = None

	def differentiate_templates(self):
		self.template_1_list = []
		self.template_2_list = []
		self.template_3_list = []
		self.template_prep = []
		self.template_verb = []

		for test_sentence in self.test_sentence_list:
			if len(test_sentence.split(' ')) == 4:
				template_1_sentence = test_sentence
				self.template_1_list.append(template_1_sentence)
			elif len(test_sentence.split(' ')) == 5:
				template_2_sentence = test_sentence
				self.template_2_list.append(template_2_sentence)
			elif len(test_sentence.split(' ')) == 3:
				template_3_sentence = test_sentence
				self.template_3_list.append(template_3_sentence)
			elif len(test_sentence.split(' ')) == 8:
				template_prep_sentence = test_sentence
				self.template_prep.append(template_prep_sentence)
			else:
				template_verb_sentence = test_sentence
				self.template_verb.append(template_verb_sentence)

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

	def replace_mask_for_template_verb(self):
		self.verb_complete = []
		for verb in self.verbs:
			for verb_sentence in self.template_verb:
				words = verb_sentence.split(" ")
				words[1] = verb
				complete_test_sentence = " ".join(words)
				self.verb_complete.append(complete_test_sentence)

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

	def count_verb_accuracy(self):
		self.accurate_pred_verb = 0
		self.accurate_sentence_verb = []

		for complete_sentence in self.verb_complete:
			words = complete_sentence.split(" ")
			if words[1] == self.verbs[0]:
				if words[3] in self.singular_list:
					self.accurate_pred_verb += 1
					self.accurate_sentence_verb.append(complete_sentence)

			elif words[1] == self.prep_verbs[1]:
				if words[3] in self.plural_list:
					self.accurate_pred_verb += 1
					self.accurate_sentence_verb.append(complete_sentence)

	def count_accuracy(self):
		self.accuracy_1_2 = int(self.accurate_pred_1) + int(self.accurate_pred_2)
		self.total_test_sentence_1_2 = len(self.sentence_1_complete) + len(self.sentence_2_complete)

	def count_proportion(self):

		try:
			self.proportion_1_2 = int(self.accuracy_1_2) / self.total_test_sentence_1_2
			self.proportion_3 = int(self.accurate_pred_3) / len(self.sentence_3_complete)
			self.proportion_prep = int(self.accurate_pred_prep) / len(self.prep_complete)

		except ZeroDivisionError:
			self.proportion_1_2 = 0
			self.proportion_3 = 0
			self.proportion_prep = 0

		try:
			self.proportion_verb = self.accurate_pred_verb / len(self.verb_complete)

		except ZeroDivisionError:
			self.proportion_verb = 0

	def print_output(self):
		# print("This is the accuracy for template_1 & template_2/ agreement_across_adjectives: {}".format(self.accuracy_1_2))
		# print("This is the proportion of correct predictions for template_1 & template_2/ agreement_across_adjectives: {}".format(
		# 	self.proportion_1_2))

		# print("This is the accuracy for template_3/ agreement_across_adjectives: {}".format(self.accurate_pred_3))
		# print("This is the proportion of correct predictions for template_3/ agreement_across_adjectives: {}".format(self.proportion_3))

		# print("This is the accuracy for agreement_across_adjectives: {}".format(self.accurate_pred_prep))
		# print("This is the proportion of correct predictions for agreement_across_adjectives: {}".format(self.proportion_prep))

		print("This is the accuracy for agreement_across_verbs: {}".format(self.accurate_pred_verb))
		print("This is the proportion of correct predictions for agreement_across_verbs: {}".format(self.proportion_verb))



def main(sentence_file_name):
	data_folder_1 = Path("/Users/vivianyu/Desktop/Babeval-master/output")
	data_folder_2 = Path("/Users/vivianyu/Desktop/Babeval-master/word_lists")
	file_name_1 = data_folder_1 / sentence_file_name # this should be one of the file from the output folder
	file_name_2 = data_folder_2 / 'nouns.txt'
	file_name_3 = data_folder_2 / 'singulars.txt'
	file_name_4 = data_folder_2 / 'plurals.txt'

	# open and read files
	with open(file_name_1) as sentence_file:
		test_sentence_list = sentence_file.read().split("\n")

	with open(file_name_2) as nouns_file:
		nouns_list = nouns_file.read().lower().split("\n")

	with open(file_name_3) as singular_file:
		singular_list = singular_file.read().lower().split("\n")

	with open(file_name_4) as plural_file:
		plural_list = plural_file.read().lower().split("\n")

	# separate start words
	start_words_singular = ["this", "that"]
	start_words_plural = ["these", "those"]
	prep_verbs = ["is", "are"]
	verbs = ["does", "do"]

	test_sentence = Test_Sentence(test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
								  start_words_plural, prep_verbs, verbs)
	test_sentence.differentiate_templates()
	test_sentence.replace_mask_for_template_1()
	test_sentence.replace_mask_for_template_2()
	test_sentence.replace_mask_for_template_3()
	test_sentence.replace_mask_for_template_prep()
	test_sentence.replace_mask_for_template_verb()
	test_sentence.count_template_1_accuracy()
	test_sentence.count_template_2_accuracy()
	test_sentence.count_template_3_accuracy()
	test_sentence.count_prep_accuracy()
	test_sentence.count_verb_accuracy()
	test_sentence.count_accuracy()
	test_sentence.count_proportion()
	test_sentence.print_output()


main(sentence_file_name = "agreement_across_verbs.txt")  # enter one of the text_file name from output folder in .txt form here



