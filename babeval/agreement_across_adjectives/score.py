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

import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ie. "look at these pretty girls" "look at these mean [UNK]"

class Agreement_Across_Adjectives:
    def __init__(self, sentence_file_name_1, sentence_file_name_2, test_sentence_list_1, test_sentence_list_2,
                 ambiguous_nouns_list, plural_list, singular_list, start_words_plural,
                 start_words_singular):

        # basic setup

        # deal with multiple sentence lists
        if test_sentence_list_2 is None:
            self.test_sentence_list = test_sentence_list_1
            self.sentence_file_name = sentence_file_name_1
        else:
            self.test_sentence_list = test_sentence_list_1 + test_sentence_list_2
            self.sentence_file_name = sentence_file_name_1 + "," + " " + sentence_file_name_2

        self.ambiguous_nouns_list = ambiguous_nouns_list
        self.plural_list = plural_list
        self.singular_list = singular_list + ['[NAME]']
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

        self.single_UNK_1 = None
        self.single_correct_1 = None
        self.single_incorrect_1 = None
        self.single_ambiguous_1 = None
        self.single_non_noun_1 = None

        # sentence with double adjectives
        self.double_UNK = None
        self.double_correct = None
        self.double_incorrect = None
        self.double_ambiguous = None
        self.double_non_noun = None

        self.double_UNK_1 = None
        self.double_correct_1 = None
        self.double_incorrect_1 = None
        self.double_ambiguous_1 = None
        self.double_non_noun_1 = None

        # sentence with three adjectives
        self.three_UNK = None
        self.three_correct = None
        self.three_incorrect = None
        self.three_ambiguous = None
        self.three_non_noun = None

        self.three_UNK_1 = None
        self.three_correct_1 = None
        self.three_incorrect_1 = None
        self.three_ambiguous_1 = None
        self.three_non_noun_1 = None

        # proportion for different sentence type

        # single
        self.single_UNK_prop = None
        self.single_correct_prop = None
        self.single_incorrect_prop = None
        self.single_ambiguous_prop = None
        self.single_non_noun_prop = None

        self.single_UNK_prop_1 = None
        self.single_correct_prop_1 = None
        self.single_incorrect_prop_1 = None
        self.single_ambiguous_prop_1 = None
        self.single_non_noun_prop_1 = None

        # double

        self.double_UNK_prop = None
        self.double_correct_prop = None
        self.double_incorrect_prop = None
        self.double_ambiguous_prop = None
        self.double_non_noun_prop = None

        self.double_UNK_prop_1 = None
        self.double_correct_prop_1 = None
        self.double_incorrect_prop_1 = None
        self.double_ambiguous_prop_1 = None
        self.double_non_noun_prop_1 = None

        # three

        self.three_UNK_prop = None
        self.three_correct_prop = None
        self.three_incorrect_prop = None
        self.three_ambiguous_prop = None
        self.three_non_noun_prop = None

        self.three_UNK_prop_1 = None
        self.three_correct_prop_1 = None
        self.three_incorrect_prop_1 = None
        self.three_ambiguous_prop_1 = None
        self.three_non_noun_prop_1 = None

        self.single_look = None
        self.double_look = None
        self.three_look = None

        self.single_no_look = None
        self.double_no_look = None
        self.three_no_look = None

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
            predicted_noun = sentence[-2]
            for word in sentence:
                if word in self.start_words:
                    start_word = word
                    adj = sentence[sentence.index(start_word) + 1:sentence.index(predicted_noun)]

            if len(adj) == 1:  # single adjective
                self.single_adj.append(sentence)

            if len(adj) == 2:  # double adjectives
                self.double_adj.append(sentence)

            if len(adj) == 3:  # three adjectives
                self.three_adj.append(sentence)

    def define_measure(self):

        self.UNK_list = []
        self.correct_list = []
        self.incorrect_list = []
        self.ambiguous_list = []
        self.non_noun_list = []

        for sentence in self.test_sentence_list:
            predicted_noun = sentence[-2]
            for word in sentence:
                if word in self.start_words:
                    start_word = word

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

        # for sentences with "look at"
        # sentence with single adjective
        self.single_UNK = []
        self.single_correct = []
        self.single_incorrect = []
        self.single_ambiguous = []
        self.single_non_noun = []

        self.single_look = []

        # sentence with double adjectives
        self.double_UNK = []
        self.double_correct = []
        self.double_incorrect = []
        self.double_ambiguous = []
        self.double_non_noun = []

        self.double_look = []

        # sentence with three adjectives
        self.three_UNK = []
        self.three_correct = []
        self.three_incorrect = []
        self.three_ambiguous = []
        self.three_non_noun = []

        self.three_look = []

        # for sentences without "look at"
        # sentence with single adjective
        self.single_UNK_1 = []
        self.single_correct_1 = []
        self.single_incorrect_1 = []
        self.single_ambiguous_1 = []
        self.single_non_noun_1 = []

        self.single_no_look = []

        # sentence with double adjectives
        self.double_UNK_1 = []
        self.double_correct_1 = []
        self.double_incorrect_1 = []
        self.double_ambiguous_1 = []
        self.double_non_noun_1 = []

        self.double_no_look = []

        # sentence with three adjectives
        self.three_UNK_1 = []
        self.three_correct_1 = []
        self.three_incorrect_1 = []
        self.three_ambiguous_1 = []
        self.three_non_noun_1 = []

        self.three_no_look = []

        for sentence in self.single_adj:
            if sentence[0] == "look":
                self.single_look.append(sentence)
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
            else:
                self.single_no_look.append(sentence)
                if sentence in self.UNK_list:
                    self.single_UNK_1.append(sentence)

                elif sentence in self.correct_list:
                    self.single_correct_1.append(sentence)

                elif sentence in self.incorrect_list:
                    self.single_incorrect_1.append(sentence)

                elif sentence in self.ambiguous_list:
                    self.single_ambiguous_1.append(sentence)

                else:
                    self.single_non_noun_1.append(sentence)

        for sentence in self.double_adj:
            if sentence[0] == "look":
                self.double_look.append(sentence)
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
            else:
                self.double_no_look.append(sentence)
                if sentence in self.UNK_list:
                    self.double_UNK_1.append(sentence)

                elif sentence in self.correct_list:
                    self.double_correct_1.append(sentence)

                elif sentence in self.incorrect_list:
                    self.double_incorrect_1.append(sentence)

                elif sentence in self.ambiguous_list:
                    self.double_ambiguous_1.append(sentence)

                else:
                    self.double_non_noun_1.append(sentence)

        for sentence in self.three_adj:
            if sentence[0] == "look":
                self.three_look.append(sentence)
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
            else:
                self.three_no_look.append(sentence)
                if sentence in self.UNK_list:
                    self.three_UNK_1.append(sentence)
                elif sentence in self.correct_list:
                    self.three_correct_1.append(sentence)
                elif sentence in self.incorrect_list:
                    self.three_incorrect_1.append(sentence)
                elif sentence in self.ambiguous_list:
                    self.three_ambiguous_1.append(sentence)
                else:
                    self.three_non_noun_1.append(sentence)

    def calculate_proportion_for_different_sentence_type(self):

        total_single = len(self.single_look)
        total_double = len(self.double_look)
        total_three = len(self.three_look)

        total_single_1 = len(self.single_no_look)
        total_double_1 = len(self.double_no_look)
        total_three_1 = len(self.three_no_look)

        # with "look at"

        # single adj
        self.single_UNK_prop = len(self.single_UNK) / total_single
        self.single_correct_prop = len(self.single_correct) / total_single
        self.single_incorrect_prop = len(self.single_incorrect) / total_single
        self.single_ambiguous_prop = len(self.single_ambiguous) / total_single
        self.single_non_noun_prop = len(self.single_non_noun) / total_single

        # double adj

        self.double_UNK_prop = len(self.double_UNK) / total_double
        self.double_correct_prop = len(self.double_correct) / total_double
        self.double_incorrect_prop = len(self.double_incorrect) / total_double
        self.double_ambiguous_prop = len(self.double_ambiguous) / total_double
        self.double_non_noun_prop = len(self.double_non_noun) / total_double

        # three adj

        self.three_UNK_prop = len(self.three_UNK) / total_three
        self.three_correct_prop = len(self.three_correct) / total_three
        self.three_incorrect_prop = len(self.three_incorrect) / total_three
        self.three_ambiguous_prop = len(self.three_ambiguous) / total_three
        self.three_non_noun_prop = len(self.three_non_noun) / total_three

        # without look at

        # single adj

        self.single_UNK_prop_1 = len(self.single_UNK_1) / total_single_1
        self.single_correct_prop_1 = len(self.single_correct_1) / total_single_1
        self.single_incorrect_prop_1 = len(self.single_incorrect_1) / total_single_1
        self.single_ambiguous_prop_1 = len(self.single_ambiguous_1) / total_single_1
        self.single_non_noun_prop_1 = len(self.single_non_noun_1) / total_single_1

        # double adj

        self.double_UNK_prop_1 = len(self.double_UNK_1) / total_double_1
        self.double_correct_prop_1 = len(self.double_correct_1) / total_double_1
        self.double_incorrect_prop_1 = len(self.double_incorrect_1) / total_double_1
        self.double_ambiguous_prop_1 = len(self.double_ambiguous_1) / total_double_1
        self.double_non_noun_prop_1 = len(self.double_non_noun_1) / total_double_1

        # three adj

        self.three_UNK_prop_1 = len(self.three_UNK_1) / total_three_1
        self.three_correct_prop_1 = len(self.three_correct_1) / total_three_1
        self.three_incorrect_prop_1 = len(self.three_incorrect_1) / total_three_1
        self.three_ambiguous_prop_1 = len(self.three_ambiguous_1) / total_three_1
        self.three_non_noun_prop_1 = len(self.three_non_noun_1) / total_three_1

    def visualize_each_sentence_type(self):
        N = 5
        ind = np.arange(5)
        width = 0.4

        x = ("[UNK]", "correct\nnoun", "incorrect\nnoun", "ambiguous\nnoun", "non-noun")
        y_1 = [self.single_UNK_prop, self.single_correct_prop, self.single_incorrect_prop, self.single_ambiguous_prop,
               self.single_non_noun_prop]
        y_2 = [self.double_UNK_prop, self.double_correct_prop, self.double_incorrect_prop, self.double_ambiguous_prop,
               self.double_non_noun_prop]
        y_3 = [self.three_UNK_prop, self.three_correct_prop, self.three_incorrect_prop, self.three_ambiguous_prop,
               self.three_non_noun_prop]

        z_1 = [self.single_UNK_prop_1, self.single_correct_prop_1, self.single_incorrect_prop_1,
               self.single_ambiguous_prop_1, self.single_non_noun_prop_1]
        z_2 = [self.double_UNK_prop_1, self.double_correct_prop_1, self.double_incorrect_prop_1,
               self.double_ambiguous_prop_1, self.double_non_noun_prop_1]
        z_3 = [self.three_UNK_prop_1, self.three_correct_prop_1, self.three_incorrect_prop_1,
               self.three_ambiguous_prop_1, self.three_non_noun_prop_1]

        fig, axs = plt.subplots(3, sharex=True, sharey=True)
        fig.suptitle(
            f'Proportion of Five Measures for Different Sentence Types\n file_name = {self.sentence_file_name}',
            fontsize=10)

        for i in range(3):
            axs[i].set_xticks(ind + width)
            axs[i].set_xticklabels(x)

        # for axs[0]
        axs[0].bar(ind, y_1, width, color='xkcd:tomato', align='center')
        axs[0].bar(ind + (width / 2), z_1, width, color='xkcd:darkblue', align='edge')
        # for axs[1]
        axs[1].bar(ind, y_2, width, color='xkcd:tomato', align='center')
        axs[1].bar(ind + (width / 2), z_2, width, color='xkcd:darkblue', align='edge')
        # for axs[2]
        axs[2].bar(ind, y_3, width, color='xkcd:tomato', align='center')
        axs[2].bar(ind + (width / 2), z_2, width, color='xkcd:darkblue', align='edge')
        # set titles
        axs[0].set_title('Sentence with Single Adjective', fontweight="bold", size=8)
        axs[1].set_title('Sentence with Two Adjectives', fontweight="bold", size=8)
        axs[2].set_title('Sentence with Three Adjectives', fontweight="bold", size=8)

        blue_patch = mpatches.Patch(color='xkcd:tomato', label='With Look At')
        green_patch = mpatches.Patch(color='xkcd:darkblue', label='Without Look At')
        fig.legend(handles=[blue_patch, green_patch], prop={'size': 6})

        fig.text(0.06, 0.5, 'proportion of total predictions that are in the category', ha='center', va='center',
                 rotation='vertical', size='small')

        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()

        plt.savefig("agreement_across_adjectives" + '.png', dpi=700)

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

    def visualize_proportion(self):
        objects = ("correct\nnoun", "incorrect\nnoun", "ambiguous\nnoun", "non-noun", "[UNK]")
        y_pos = np.arange(len(objects))
        y_bar = [self.correct_proportion, self.incorrect_proportion, self.ambiguous_proportion,
                 self.non_noun_proportion, self.UNK_proportion]

        plt.bar(y_pos, y_bar, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Proportions')
        plt.title(f'Agreement_Across_Adjectives\nn={len(self.test_sentence_list)}')
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        # plt.savefig('xxx.png', dpi=700)
        plt.show()

    def print_output(self):

        y_1 = [self.single_UNK_prop, self.single_correct_prop, self.single_incorrect_prop, self.single_ambiguous_prop,
               self.single_non_noun_prop]
        y_2 = [self.double_UNK_prop, self.double_correct_prop, self.double_incorrect_prop, self.double_ambiguous_prop,
               self.double_non_noun_prop]
        y_3 = [self.three_UNK_prop, self.three_correct_prop, self.three_incorrect_prop, self.three_ambiguous_prop,
               self.three_non_noun_prop]

        z_1 = [self.single_UNK_prop_1, self.single_correct_prop_1, self.single_incorrect_prop_1,
               self.single_ambiguous_prop_1, self.single_non_noun_prop_1]
        z_2 = [self.double_UNK_prop_1, self.double_correct_prop_1, self.double_incorrect_prop_1,
               self.double_ambiguous_prop_1, self.double_non_noun_prop_1]
        z_3 = [self.three_UNK_prop_1, self.three_correct_prop_1, self.three_incorrect_prop_1,
               self.three_ambiguous_prop_1, self.three_non_noun_prop_1]

        labels = ["UNK", "Correct", "Incorrect", "Ambiguous", "Non-Noun"]

        print("\nWith 'look-at' Sentences:")
        print("\nSingle Adjective: ")

        for l, y in zip(labels, y_1):
            print("{}: {}".format(l, y))

        print("\nTwo Adjectives: ")

        for l, y in zip(labels, y_2):
            print("{}: {}".format(l, y))

        print("\nThree Adjectives: ")

        for l, y in zip(labels, y_3):
            print("{}: {}".format(l, y))

        print("\nWithout 'look-at' Sentences")
        print("\nSingle Adjective: ")

        for l, z in zip(labels, z_1):
            print("{}: {}".format(l, z))

        print("\nTwo Adjectives: ")

        for l, z in zip(labels, z_2):
            print("{}: {}".format(l, z))

        print("\nThree Adjectives: ")

        for l, z in zip(labels, z_3):
            print("{}: {}".format(l, z))


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


def main(sentence_file_name_1, sentence_file_name_2):
    data_folder_1 = Path().cwd()
    file_name_1 = data_folder_1 / 'nouns_annotator2.txt'
    file_name_2 = data_folder_1 / 'nouns_singular_annotator2.txt'
    file_name_3 = data_folder_1 / 'nouns_plural_annotator2.txt'
    file_name_4 = data_folder_1 / 'nouns_ambiguous_number_annotator2.txt'

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

    if sentence_file_name_2 is None:
        test_sentence_list_1 = format_BERT_output(sentence_file_name_1)
        test_sentence_list_2 = None
    else:
        test_sentence_list_1 = format_BERT_output(sentence_file_name_1)
        test_sentence_list_2 = format_BERT_output(sentence_file_name_2)

    # separate start words
    start_words_singular = ["this", "that"]
    start_words_plural = ["these", "those"]
    prep_verbs = ["is", "are"]
    verbs = ["does", "do"]

    # Counting number agreements for agreement_across_adjectives:
    agreement_across_adj = Agreement_Across_Adjectives(sentence_file_name_1, sentence_file_name_2, test_sentence_list_1,
                                                       test_sentence_list_2, ambiguous_nouns_list, plural_list,
                                                       singular_list, start_words_plural, start_words_singular)
    agreement_across_adj.identify_numbers_of_adj()
    agreement_across_adj.define_measure()
    agreement_across_adj.finding_different_sentence_type()
    agreement_across_adj.calculate_proportion_for_different_sentence_type()
    agreement_across_adj.visualize_each_sentence_type()
    agreement_across_adj.calculate_overall_proportion()
    agreement_across_adj.visualize_proportion()
    agreement_across_adj.print_output()


main(sentence_file_name_1="look-at-the_47000.txt", sentence_file_name_2="47000.txt")
# enter the both BERT ouput file here to score accuracy
