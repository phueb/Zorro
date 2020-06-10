"""
#u: BERT gives [UNK] for predicted_prep_verb
#c: number agreement between targeted_noun and predicted_prep_verb
#f: number disagreement between targeted_noun and predicted_prep_verbs
#n: Predictions given by BERT are non-prep_verbs
"""
from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions

prediction_file_names = [
    'probing_agreement_across_PP_results_80000_with_srl.txt',
    'probing_agreement_across_PP_results_80000_no_srl.txt'
]

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
template2file_name2props = score_predictions(prediction_file_names,
                                             templates,
                                             categorize_templates,
                                             categorize_predictions,
                                             print_stats)

# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2file_name2props)