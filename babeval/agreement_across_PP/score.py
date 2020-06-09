from pathlib import Path

from babeval.reader import Reader
from babeval.visualizer import Visualizer

prep_verbs = ["is", "are"]

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

def categorize_predictions(test_sentence_list):
    res = {'u': [ ], 'c':[ ], 'f': [ ]}

#u: BERT gives [UNK] for predicted_prep_verb
#c: number agreement between targeted_noun and predicted_prep_verb
#f: number disagreement between targeted_noun and predicted_prep_verbs
#n: Predictions given by BERT are non-prep_verbs

    for sentence in test_sentence_list:
        predicted_prep_verb = [w for w in sentence if w in prep_verbs]
        targeted_noun = sentence[1]

        # [UNK] CONDITION
        if predicted_prep_verb == "[UNK]":
            res.setdefault('u', []).append(sentence)

        # correct Prep Verbs
        elif targeted_noun in nouns_plural and predicted_prep_verb == "are":
            res.setdefault('c', []).append(sentence)

        elif targeted_noun in nouns_singular and predicted_prep_verb == "is":
            res.setdefault('c', []).append(sentence)

        # false Prep Verbs
        elif targeted_noun in nouns_plural and predicted_prep_verb == "is":
            res.setdefault('f', []).append(sentence)

        elif targeted_noun in nouns_singular and predicted_prep_verb == "are":
            res.setdefault('f', []).append(sentence)

        # Non-prep_verbs
        else:
            res.setdefault('n', []).append(sentence)

    return res

def print_stats(sentences):
    num_singular = 0
    num_plural = 0
    num_total = 0  
    for s in sentences:
        targeted_noun = s[1] # only counting the targeted noun 
        if targeted_noun in nouns_list:
            num_total += 1
        if targeted_noun in nouns_singular:
            num_singular += 1
        elif targeted_noun in nouns_plural:
            num_plural += 1
        else:
            raise RuntimeError(f'{w} is neither in plural or singular or ambiguous nouns list')
    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')


def main(*sentence_file_names):

    types = ["u", "c", "f", "n"]

    control_name = '_frequency-based control'
    sentence_file_names = list(sentence_file_names) + \
                          [name + control_name for name in sentence_file_names]
    fig_data = {fn: [] for fn in sentence_file_names} 

    for sentence_file_name in sentence_file_names:
        print(f'Scoring {sentence_file_name}')

        if sentence_file_name.endswith(control_name):
            reader = Reader(sentence_file_name.replace(control_name, ''))
            sentences = reader.rand_predictions
            print_stats(sentences)
        else:
            reader = Reader(sentence_file_name)
            sentences = reader.bert_predictions
            print_stats(sentences)

        predictions = categorize_predictions(sentences)  # categorize into four categories
        for category, sentences_in_category in predictions.items():
            prop = len(sentences_in_category) / len(sentences)
            fig_data[sentence_file_name].append(prop)

    print(fig_data)

    # plot
    visualizer = Visualizer()
    xtick_labels = ("[UNK]", "correct\nprep_verbs", "false\nprep_verbs", "non-prep_verbs")
    visualizer.make_barplot(xtick_labels, fig_data)

    #TODO: visualizer not applicable because fig_data was composed of list


# main('probing_agreement_across_adjectives_results_100000_no_srl.txt')

main("","") # Two agreement_across_PP files 


