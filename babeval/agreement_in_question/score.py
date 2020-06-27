"""
Example sentences in task:
where [MASK] the afternoon go ? do/does
where [MASK] the alouette ? is/are

Predictions are categorized as follows:
[UNK]: BERT gives [UNK] as prediction to [MASK]
Correct Verb: number agreement between [MASK] and targeted noun
Incorrect Verb: number disagreement between [MASK] and targeted noun
Non-verb: prediction given by BERT is not in targeted verb
"""
from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions
from babeval.io import get_group2predictions_file_paths

DUMMY = False

task_name = Path(__file__).parent.name
group2predictions_file_paths = get_group2predictions_file_paths(DUMMY, task_name)

subjective_copula_singular = ["does", "is", "'s"]
subjective_copula_plural = ["do", "are", "'re"]

templates = ['Sentence with go',
             'Sentence without go',
             ]

prediction_categories = ("[UNK]", "correct\nverb", "false\nverb", "non-verb")

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


def categorize_by_template(sentences_in, sentences_out):
    """
    differentiate sentences with or without "go"
    :param sentences_in:
    :param sentences_out:
    :return:
    """

    res = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        for w in s1:
            if w == 'go':
                res.setdefault(templates[0], []).append(s2)
            else:
                res.setdefault(templates[1], []).append(s2)
        else:
            raise RuntimeError('Failed to categorize sentence into template')

    return res


def categorize_predictions(test_sentence_list):
    res = {}

    for sentence in test_sentence_list:
        predicted_verb = sentence[1] #[MASK]
        targeted_noun = sentence[3] #noun from test sentence
        res = {'u': [], 'c': [], 'f': [], 'n': []}

        # [UNK]
        if predicted_verb == "[UNK]":
            res['u'].append(sentence)

        # correct Noun Number
        elif targeted_noun in nouns_plural and predicted_verb in subjective_copula_plural:
            res['c'].append(sentence)

        elif targeted_noun in nouns_singular and predicted_verb in subjective_copula_singular:
            res['c'].append(sentence)

        # false Noun Number
        elif targeted_noun in nouns_plural and predicted_verb in subjective_copula_singular:
            res['f'].append(sentence)

        elif targeted_noun in nouns_singular and predicted_verb in subjective_copula_plural:
            res['f'].append(sentence)

        # Non_Noun
        else:
            res['n'].append(sentence)

    return res


def print_stats(sentences):
    pass

# score
template2group_name2props = score_predictions(group2predictions_file_paths,
                                              templates,
                                              categorize_by_template,
                                              categorize_predictions,
                                              print_stats)

# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2group_name2props)