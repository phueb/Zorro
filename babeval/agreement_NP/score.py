"""
Score predictions made by language model.
"""
class Test_Sentence:
	def __init__(self, test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
				 start_words_plural):
		self.test_sentence_list = test_sentence_list
		self.nouns_list = nouns_list
		self.singular_list = singular_list
		self.plural_list = plural_list
		self.start_words_singular = start_words_singular
		self.start_words_plural = start_words_plural
		self.template_1_list = None
		self.template_2_list = None
		self.template_3_list = None
		self.sentence_1_complete = None
		self.sentence_2_complete = None
		self.sentence_3_complete = None
		self.accurate_pred_1 = None
		self.accurate_pred_2 = None
		self.accurate_pred_3 = None
		self.accurate_sentence_1 = None
		self.accurate_sentence_2 = None
		self.accurate_sentence_3 = None
		self.accuracy = None
		self.total_test_sentence = None
		self.accuracy_proportion = None

	def differentiate_templates(self):
		self.template_1_list = []
		self.template_2_list = []
		self.template_3_list = []

		for test_sentence in self.test_sentence_list:
			if len(test_sentence.split(' ')) == 3:
				template_1_sentence = test_sentence
				self.template_1_list.append(template_1_sentence)
			elif len(test_sentence.split(' ')) == 4:
				template_2_sentence = test_sentence
				self.template_2_list.append(template_2_sentence)
			else:
				template_3_sentence = test_sentence
				self.template_3_list.append(template_3_sentence)

	def replace_masks_for_template_1(self):
		self.sentence_1_complete = []
		for noun in self.nouns_list:
			for sentence_1 in self.template_1_list:
				words = sentence_1.split(" ")
				words[2] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_1_complete.append(complete_test_sentence)

	def replace_masks_for_template_2(self):
		self.sentence_2_complete = []
		for noun in self.nouns_list:
			for sentence_2 in self.template_2_list:
				words = sentence_2.split(" ")
				words[3] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_2_complete.append(complete_test_sentence)

	def replace_masks_for_template_3(self):
		self.sentence_3_complete = []
		for noun in self.nouns_list:
			for sentence_3 in self.template_3_list:
				words = sentence_3.split(" ")
				words[1] = noun
				complete_test_sentence = " ".join(words)
				self.sentence_3_complete.append(complete_test_sentence)

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

	def count_accuracy(self):
		self.accuracy = self.accurate_pred_1 + self.accurate_pred_2 + self.accurate_pred_3

	def count_proportion(self):
		self.total_test_sentence = len(self.sentence_1_complete) + len(self.sentence_2_complete) + len(
			self.sentence_3_complete)
		self.proportion = self.accuracy / self.total_test_sentence

	def print_output(self):
		print("This is the accuracy {}".format(self.accuracy))
		print("This is the proportion of correct predictions {}".format(self.proportion))

def main(sentence_file_name):
	# basic setup
	file_name_1 = sentence_file_name
	file_name_2 = 'nouns.txt'
	file_name_3 = 'singular.txt'
	file_name_4 = 'plural.txt'

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

	test_sentence = Test_Sentence(test_sentence_list, nouns_list, singular_list, plural_list, start_words_singular,
								  start_words_plural)
	test_sentence.differentiate_templates()
	test_sentence.replace_masks_for_template_1()
	test_sentence.replace_masks_for_template_2()
	test_sentence.replace_masks_for_template_3()
	test_sentence.count_template_1_accuracy()
	test_sentence.count_template_2_accuracy()
	test_sentence.count_template_3_accuracy()
	test_sentence.count_accuracy()
	test_sentence.count_proportion()
	test_sentence.print_output()

main(sentence_file_name="")  # enter text_file name in .txt form here




