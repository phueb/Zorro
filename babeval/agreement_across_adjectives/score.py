"""
Score predictions made by language model.
The agreement_across_adjectives task should not just calcualte a single accuracy measure, but calculate 5 measures, each quantifying the proportion of model-predictions that correspond to a particular kind of answer:
1. correct noun number
2. incorrect noun number
3. ambiguous noun number ("sheep", "fish")
4. non-noun
5. [UNK] (this means "unknown", which means the model doesn't want to commit to an answer)

it can handle a file that has sentences with different amounts of adjectives (1, 2, 3) ?
And sentences with "look at ..." and without.
"""
from pathlib import Path

import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.text as Text


# ie. "look at these pretty girls" "look at these mean [UNK]"

class Agreement_Across_Adjectives:
    def __init__(self, test_sentence_list, ambiguous_nouns_list, plural_list, singular_list, start_words_plural,
                 start_words_singular):

        # basic setup
        self.test_sentence_list = test_sentence_list
        self.ambiguous_nouns_list = ambiguous_nouns_list
        self.plural_list = plural_list
        self.singular_list = singular_list + ['[NAME]', 'one']
        self.start_words_plural = start_words_plural
        self.start_words_singular = start_words_singular
        self.start_words = self.start_words_plural + self.start_words_singular

        # differentiate sentences based on numbers of adjectives
        self.single_adj = None
        self.double_adj = None
        self.three_adj = None

        # define measure
        self.UNK_list = None
        self.correct_list = None
        self.incorrect_list = None
        self.ambiguous_list = None
        self.non_noun_list = None

        # sentence with single adjective
        self.single_UNK = None
        self.single_correct = None
        self.single_incorrect = None
        self.single_ambiguous = None
        self.single_non_noun = None

        # sentence with double adjectives
        self.double_UNK = None
        self.double_correct = None
        self.double_incorrect = None
        self.double_ambiguous = None
        self.double_non_noun = None

        # sentence with three adjectives
        self.three_UNK = None
        self.three_correct = None
        self.three_incorrect = None
        self.three_ambiguous = None
        self.three_non_noun = None

        # proportion for different sentence type

        # single
        self.single_UNK_prop = None
        self.single_correct_prop = None
        self.single_incorrect_prop = None
        self.single_ambiguous_prop = None
        self.single_non_noun_prop = None

        # double

        self.double_UNK_prop = None
        self.double_correct_prop = None
        self.double_incorrect_prop = None
        self.double_ambiguous_prop = None
        self.double_non_noun_prop = None

        # three

        self.three_UNK_prop = None
        self.three_correct_prop = None
        self.three_incorrect_prop = None
        self.three_ambiguous_prop = None
        self.three_non_noun_prop = None

        # total prediction and proportion
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

    def identify_numbers_of_adj(self):

        self.single_adj = []
        self.double_adj = []
        self.three_adj = []

        for sentence in self.test_sentence_list:

            for i in sentence:
                if i in self.start_words:
                    start_word = i
            predicted_noun = sentence[-1]

            # finding numbers of adjectives in between start_word and predicted_noun

            adj = sentence[sentence.index(start_word) + len(start_word):sentence.index(predicted_noun)]
            filter_object = filter(lambda x: x != "", adj)
            clear_adj = list(filter_object)

            if len(clear_adj) == 1:  # single adjective
                self.single_adj.append(sentence)

            if len(clear_adj) == 2:  # double adjectives
                self.double_adj.append(sentence)

            if len(clear_adj) == 3:  # three adjectives
                self.three_adj.append(sentence)

    def define_measure(self):

        self.UNK_list = []
        self.correct_list = []
        self.incorrect_list = []
        self.ambiguous_list = []
        self.non_noun_list = []

        for sentence in self.test_sentence_list:
            # sentence is a list

            # this should avoid hard-code
            for i in sentence:
                if i in self.start_words:
                    start_word = i

            predicted_noun = sentence[-2]
            print(sentence)
            print(predicted_noun)

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

    def finding_different_sentence_type(self):

        # sentence with single adjective
        self.single_UNK = []
        self.single_correct = []
        self.single_incorrect = []
        self.single_ambiguous = []
        self.single_non_noun = []

        # sentence with double adjectives
        self.double_UNK = []
        self.double_correct = []
        self.double_incorrect = []
        self.double_ambiguous = []
        self.double_non_noun = []

        # sentence with three adjectives
        self.three_UNK = []
        self.three_correct = []
        self.three_incorrect = []
        self.three_ambiguous = []
        self.three_non_noun = []

        for sentence in self.single_adj:
            if sentence in self.UNK_list:
                self.single_UNK.append(sentence)
            elif sentence in self.correct_list:
                self.single_correct.append(sentence)
            elif sentence in self.incorrect_list:
                self.single_incorrect.append(sentence)
            elif sentence in self.ambiguous_list:
                self.single_ambiguous.append(sentence)
            else:
                self.single_non_noun.append(sentence)

        for sentence in self.double_adj:
            if sentence in self.UNK_list:
                self.double_UNK.append(sentence)
            elif sentence in self.correct_list:
                self.double_correct.append(sentence)
            elif sentence in self.incorrect_list:
                self.double_incorrect.append(sentence)
            elif sentence in self.ambiguous_list:
                self.double_ambiguous.append(sentence)
            else:
                self.double_non_noun.append(sentence)

        for sentence in self.three_adj:
            if sentence in self.UNK_list:
                self.three_UNK.append(sentence)
            elif sentence in self.correct_list:
                self.three_correct.append(sentence)
            elif sentence in self.incorrect_list:
                self.three_incorrect.append(sentence)
            elif sentence in self.ambiguous_list:
                self.three_ambiguous.append(sentence)
            else:
                self.three_non_noun.append(sentence)

    def calculate_proportion_for_different_sentence_type(self):
        # single adj
        total_single = len(self.single_adj)

        self.single_UNK_prop = len(self.single_UNK) / total_single
        self.single_correct_prop = len(self.single_correct) / total_single
        self.single_incorrect_prop = len(self.single_incorrect) / total_single
        self.single_ambiguous_prop = len(self.single_ambiguous) / total_single
        self.single_non_noun_prop = len(self.single_non_noun) / total_single

        # double adj
        total_double = len(self.double_adj)

        self.double_UNK_prop = len(self.double_UNK) / total_single
        self.double_correct_prop = len(self.double_correct) / total_single
        self.double_incorrect_prop = len(self.double_incorrect) / total_single
        self.double_ambiguous_prop = len(self.double_ambiguous) / total_single
        self.double_non_noun_prop = len(self.double_non_noun) / total_single

        # three adj
        total_three = len(self.three_adj)

        self.three_UNK_prop = len(self.three_UNK) / total_single
        self.three_correct_prop = len(self.three_correct) / total_single
        self.three_incorrect_prop = len(self.three_incorrect) / total_single
        self.three_ambiguous_prop = len(self.three_ambiguous) / total_single
        self.three_non_noun_prop = len(self.three_non_noun) / total_single

    def visualize_each_sentence_type(self):
        x = ("correct\nnoun", "incorrect\nnoun", "ambiguous\nnoun", "non-noun", "[UNK]")
        y_1 = [self.single_UNK_prop, self.single_correct_prop, self.single_incorrect_prop, self.single_ambiguous_prop,
               self.single_non_noun_prop]
        y_2 = [self.double_UNK_prop, self.double_correct_prop, self.double_incorrect_prop, self.double_ambiguous_prop,
               self.double_non_noun_prop]
        y_3 = [self.three_UNK_prop, self.three_correct_prop, self.three_incorrect_prop, self.three_ambiguous_prop,
               self.three_non_noun_prop]

        fig, axs = plt.subplots(3, sharex=True, sharey=True)
        # fig.suptitle('Proportion of five measures for different sentence types')
        axs[0].plot(x, y_1)
        axs[1].plot(x, y_2)
        axs[2].plot(x, y_3)

        axs[0].set_title('Sentence with Single Adjective', fontweight="bold", size=8)
        axs[1].set_title('Sentence with Two Adjectives', fontweight="bold", size=8)
        axs[2].set_title('Sentence with Three Adjectives', fontweight="bold", size=8)

        # fig.text(0.5, 0.04, 'types of measures', ha='center', va='center', size='small')
        # fig.text(0.06, 0.5, 'proportion of total predictions that are in the category', ha='center', va='center',
        #          rotation='vertical', size='small')

        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()

        plt.show()

    def calculate_overall_proportion(self):
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
        plt.ylim([0, 0.5])
        plt.ylabel('proportion of total predictions that are in the category')
        plt.title(f'Agreement_Across_Adjectives\nn={len(self.test_sentence_list)}\n{sentence_file_name}')
        # mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()
        # plt.savefig('figure1.png', dpi=700)
        plt.show()

    def print_output(self):

        print("\nSingle Adjective: ")
        print("[UNK]: {}".format(self.single_UNK_prop))
        print("correct noun: {}".format(self.single_correct_prop))
        print("incorrect noun: {}".format(self.single_incorrect_prop))
        print("ambiguous noun: {}".format(self.single_ambiguous_prop))
        print("non_noun: {}".format(self.single_non_noun_prop))

        print("\nTwo Adjectives: ")
        print("[UNK]: {}".format(self.double_UNK_prop))
        print("correct noun: {}".format(self.double_correct_prop))
        print("incorrect noun: {}".format(self.double_incorrect_prop))
        print("ambiguous noun: {}".format(self.double_ambiguous_prop))
        print("non_noun: {}".format(self.double_non_noun_prop))

        print("\nThree Adjectives: ")
        print("[UNK]: {}".format(self.three_UNK_prop))
        print("correct noun: {}".format(self.three_correct_prop))
        print("incorrect noun: {}".format(self.three_incorrect_prop))
        print("ambiguous noun: {}".format(self.three_ambiguous_prop))
        print("non_noun: {}".format(self.three_non_noun_prop))


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
    agreement_across_adj.identify_numbers_of_adj()
    agreement_across_adj.define_measure()
    agreement_across_adj.finding_different_sentence_type()
    agreement_across_adj.calculate_proportion_for_different_sentence_type()
    agreement_across_adj.visualize_each_sentence_type()
    agreement_across_adj.calculate_overall_proportion()
    agreement_across_adj.visualize_proportion(sentence_file_name)
    agreement_across_adj.print_output()


main("47000.txt")  # enter the BERT ouput file here to score accuracy
# main("look-at-the_47000.txt")  # enter the BERT ouput file here to score accuracy
