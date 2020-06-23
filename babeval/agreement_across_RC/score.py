from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions
from babeval.io import get_group2predictions_file_paths

DUMMY = False

task_name = Path(__file__).parent.name
group2predictions_file_paths = get_group2predictions_file_paths(DUMMY, task_name)

copulas_singular = ["is", "'s"]
copulas_plural = ["are", "'re"]

templates = ['default',
             ]

prediction_categories = ("[UNK]", "correct\ncopula", "false\ncopula", "non-copula")

# load word lists
with (Path().cwd() / 'nouns_annotator2.txt').open() as f:
    nouns_list = f.read().split("\n")
with (Path().cwd() / 'nouns_singular_annotator2.txt').open() as f:
    nouns_singular = f.read().split("\n")
with (Path().cwd() / 'nouns_plural_annotator2.txt').open() as f:
    nouns_plural = f.read().split("\n")

assert '[NAME]' in nouns_singular

for w in nouns_singular:
    assert w not in nouns_plural

for w in nouns_plural:
    assert w not in nouns_singular


def categorize_templates(test_sentence_list):

    res = {}

    for sentence in test_sentence_list:
        res.setdefault(templates[0], []).append(sentence)
    return res


def categorize_predictions(test_sentence_list):
    res = {'u': [], 'c': [], 'f': [], 'n': []}

    for sentence in test_sentence_list:
        predicted_word = sentence[-3] 
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
                                              categorize_templates,
                                              categorize_predictions,
                                              print_stats)
# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2group_name2props)