"""
#u: BERT gives [UNK] for predicted_prep_verb
#c: number agreement between targeted_noun and predicted_prep_verb
#f: number disagreement between targeted_noun and predicted_prep_verbs
#n: Predictions given by BERT are non-prep_verbs
"""
from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions
from babeval.io import get_group2predictions_file_paths

DUMMY = True

task_name = Path(__file__).parent.name
group2predictions_file_paths = get_group2predictions_file_paths(DUMMY, task_name)

copulas_singular = ["is", "'s"]
copulas_plural = ["are", "'re"]

templates = ['default',
             ]

prediction_categories = ("[UNK]", "correct\ncopula", "false\ncopula", "non-copula")

# load word lists
with (Path(__file__).parent / 'word_lists' / 'nouns_annotator2.txt').open() as f:
    nouns_list = f.read().split("\n")
with (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open() as f:
    nouns_singular = f.read().split("\n")
with (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open() as f:
    nouns_plural = f.read().split("\n")

assert '[NAME]' in nouns_singular

for w in nouns_singular:
    assert w not in nouns_plural

for w in nouns_plural:
    assert w not in nouns_singular


def categorize_by_template(sentences_in, sentences_out):

    res = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        res.setdefault(templates[0], []).append(s2)
    return res


def categorize_predictions(test_sentence_list):
    res = {'u': [], 'c': [], 'f': [], 'n': []}

    for sentence in test_sentence_list:
        predicted_word = sentence[-3]  # predicted word may not be a copula ("is", "are")
        targeted_noun = sentence[1]

        # [UNK]
        if predicted_word == "[UNK]":
            res['u'].append(sentence)

        # correct copula
        elif targeted_noun in nouns_plural and predicted_word in copulas_plural:
            res['c'].append(sentence)

        elif targeted_noun in nouns_singular and predicted_word in copulas_singular:
            res['c'].append(sentence)

        # false copula
        elif targeted_noun in nouns_plural and predicted_word in copulas_singular:
            res['f'].append(sentence)

        elif targeted_noun in nouns_singular and predicted_word in copulas_plural:
            res['f'].append(sentence)

        # Non-copula
        else:
            res['n'].append(sentence)

    return res


def print_stats(sentences):
    print('Done')


# score
template2group_name2props = score_predictions(group2predictions_file_paths,
                                              templates,
                                              categorize_by_template,
                                              categorize_predictions,
                                              print_stats)

# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2group_name2props)