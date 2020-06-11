# where [MASK] the afternoon go ? do/does
# where [MASK] the alouette ? is/are

# [UNK]: BERT gives [UNK] as prediction to [MASK]
# Correct Verb: number agreement between [MASK] and targeted noun
# Incorrect Verb: number disagreement between [MASK] and targeted noun
# Non-verb: prediction given by BERT is not in targeted verb

from pathlib import Path

from babeval.visualizer import Visualizer
from babeval.scoring import score_predictions


prediction_file_names = [
    '(dummy)probing_agreement_in_question_results_80000_with_srl.txt',
    '(dummy)probing_agreement_in_question_results_80000_no_srl.txt'
]

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


def categorize_templates(test_sentence_list):
    # differentiate sentences with or without "go"

    res = {}
    go = ['go']

    for sentence in test_sentence_list:
        for w in sentence:
            if w in go:
                res.setdefault(templates[0], []).append(sentence)
            else:
                res.setdefault(templates[1], []).append(sentence)

        # break  # exit inner for loop

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
    num_singular = 0
    num_plural = 0
    num_ambiguous = 0
    num_total = 0
    for s in sentences:
        for w in s:
            if w in nouns_list:
                num_total += 1
                if w in nouns_singular:
                    num_singular += 1
                elif w in nouns_plural:
                    num_plural += 1
                else:
                    raise RuntimeError(f'{w} is neither in plural or singular or ambiguous nouns list')
    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')


# score
template2file_name2props = score_predictions(prediction_file_names,
                                             templates,
                                             categorize_templates,
                                             categorize_predictions,
                                             print_stats)

# plot
visualizer = Visualizer()
visualizer.make_barplot(prediction_categories, template2file_name2props)