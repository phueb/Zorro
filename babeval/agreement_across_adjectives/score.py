"""
Score predictions made by language model.
The agreement_across_adjectives task should not just calcualte a 1 accuracy measure, but calculate 5 measures, each quantifying the proportion of model-predictions that correspond to a particular kind of answer:
1. c noun number
2. f noun number
3. ambiguous noun number ("sheep", "fish")
4. non-noun
5. [UNK] (this means "unknown", which means the model doesn't want to commit to an answer)

it can handle a file that has sentences with different amounts of adjectives (1, 2, 3) ?
And sentences with "look at ..." and without.
"""
from pathlib import Path
import matplotlib.pyplot as plt

from babeval.reader import Reader
from babeval.visualizer import Visualizer

plt.rcdefaults()

# start words
start_words_singular = ["this", "that"]
start_words_plural = ["these", "those"]
start_words = start_words_singular + start_words_plural

# load word lists
with (Path().cwd() / 'nouns_annotator2.txt').open() as f:
    nouns_list = f.read().split("\n")
with (Path().cwd() / 'nouns_singular_annotator2.txt').open() as f:
    nouns_singular = f.read().split("\n")
with (Path().cwd() / 'nouns_plural_annotator2.txt').open() as f:
    nouns_plural = f.read().split("\n")
with (Path().cwd() / 'nouns_ambiguous_number_annotator2.txt').open() as f:
    ambiguous_nouns = f.read().split("\n")

assert '[NAME]' in nouns_singular


def categorize_sentences(test_sentence_list):

    res = {}

    for sentence in test_sentence_list:
        predicted_noun = sentence[-2]
        for word in sentence:
            if word in start_words:
                start_word = word
                adj = sentence[sentence.index(start_word) + 1:sentence.index(predicted_noun)]

                if len(adj) == 1:  # 1 adjective
                    res.setdefault('1', []).append(sentence)

                if len(adj) == 2:  # 2 adjectives
                    res.setdefault('2', []).append(sentence)

                if len(adj) == 3:  # 3 adjectives
                    res.setdefault('3', []).append(sentence)

                break  # exit inner for loop

    return res


def categorize_predictions(test_sentence_list):

    res = {}

    for sentence in test_sentence_list:
        predicted_noun = sentence[-2]
        start_word = [w for w in start_words if w in start_words][0]

        # [UNK] CONDITION
        if predicted_noun == "[UNK]":
            res.setdefault('u', []).append(sentence)

        # c Noun Number
        elif predicted_noun in nouns_plural and start_word in start_words_plural:
            res.setdefault('c', []).append(sentence)

        elif predicted_noun in nouns_singular and start_word in start_words_singular:
            res.setdefault('c', []).append(sentence)

        # f Noun Number
        elif predicted_noun in nouns_plural and start_word in start_words_singular:
            res.setdefault('f', []).append(sentence)

        elif predicted_noun in nouns_singular and start_word in start_words_plural:
            res.setdefault('f', []).append(sentence)

        # Ambiguous Noun
        elif predicted_noun in ambiguous_nouns:
            res.setdefault('a', []).append(sentence)

        # Non_Noun
        else:
            res.setdefault('n', []).append(sentence)

    return res


def main(*sentence_file_names):
    
    data = {}
    
    for sentence_file_name in sentence_file_names:
        reader = Reader(sentence_file_name)
        sentences = categorize_sentences(reader.test_sentence_list)  # into num adjectives
    
        for num_adjectives in ['1', '2', '3']:
            predictions = categorize_predictions(sentences[num_adjectives])  # into 5 categories

            for category, sentences_in_category in predictions.items():
                key = f'{num_adjectives}_{category}'
                print(key)
                prop = len(sentences_in_category) / len(sentences[num_adjectives])
                data.setdefault(key, []).append(prop)
    
    # prepare data for plotting bars
    xtick_labels = ("[UNK]", "correct\nnoun", "false\nnoun", "ambiguous\nnoun", "non-noun")
    y1 = [data.get('1_u', [0.0] * len(sentence_file_names))[0],
          data.get('1_c', [0.0] * len(sentence_file_names))[0],
          data.get('1_f', [0.0] * len(sentence_file_names))[0],
          data.get('1_a', [0.0] * len(sentence_file_names))[0],
          data.get('1_n', [0.0] * len(sentence_file_names))[0]]
    y2 = [data.get('2_u', [0.0] * len(sentence_file_names))[0],
          data.get('2_c', [0.0] * len(sentence_file_names))[0],
          data.get('2_f', [0.0] * len(sentence_file_names))[0],
          data.get('2_a', [0.0] * len(sentence_file_names))[0],
          data.get('2_n', [0.0] * len(sentence_file_names))[0]]
    y3 = [data.get('3_u', [0.0] * len(sentence_file_names))[0],
          data.get('3_c', [0.0] * len(sentence_file_names))[0],
          data.get('3_f', [0.0] * len(sentence_file_names))[0],
          data.get('3_a', [0.0] * len(sentence_file_names))[0],
          data.get('3_n', [0.0] * len(sentence_file_names))[0]]

    z1 = [data.get('1_u', [0.0] * len(sentence_file_names))[1],
          data.get('1_c', [0.0] * len(sentence_file_names))[1],
          data.get('1_f', [0.0] * len(sentence_file_names))[1],
          data.get('1_a', [0.0] * len(sentence_file_names))[1],
          data.get('1_n', [0.0] * len(sentence_file_names))[1]]
    z2 = [data.get('2_u', [0.0] * len(sentence_file_names))[1],
          data.get('2_c', [0.0] * len(sentence_file_names))[1],
          data.get('2_f', [0.0] * len(sentence_file_names))[1],
          data.get('2_a', [0.0] * len(sentence_file_names))[1],
          data.get('2_n', [0.0] * len(sentence_file_names))[1]]
    z3 = [data.get('3_u', [0.0] * len(sentence_file_names))[1],
          data.get('3_c', [0.0] * len(sentence_file_names))[1],
          data.get('3_f', [0.0] * len(sentence_file_names))[1],
          data.get('3_a', [0.0] * len(sentence_file_names))[1],
          data.get('3_n', [0.0] * len(sentence_file_names))[1]]

    # plot
    visualizer = Visualizer()
    visualizer.make_barplot(xtick_labels, y1, y2, y3, z1, z2, z3, sentence_file_names)



main('probing_agreement_across_adjectives_results_100000_no_srl.txt',
     'probing_agreement_across_adjectives_results_100000_with_srl.txt')
