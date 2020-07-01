"""
Score predictions made by BERT on agreement across adjectives task.
"""
from pathlib import Path

from babeval.scoring import score_predictions
from babeval.io import get_group2predictions_file_paths

PRINT_STATS = False

task_name = Path(__file__).parent.name
group2predictions_file_paths = get_group2predictions_file_paths(task_name)

start_words_singular = ["this", "that"]
start_words_plural = ["these", "those"]
start_words = set(start_words_singular + start_words_plural)

templates = ['1 Adjective(s)',
             '2 Adjective(s)',
             '3 Adjective(s)',
             ]

prediction_categories = (
    "noun +\ncorrect number",
    "noun +\nfalse number",
    "noun +\n ambiguous number",
    "noun\nproper",
    "non-start\nword-piece\nor\n[UNK]",
    "non-noun",
)

# load word lists
nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split("\n")
nouns_ambiguous = (Path(__file__).parent / 'word_lists' / 'nouns_ambiguous_number_annotator2.txt').open().read().split("\n")

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

nouns_singular += ['one']

# move proper nouns to separate set
nouns_proper = set([n for n in nouns_singular if n.istitle()])
nouns_proper.add('[NAME]')
nouns_singular = [n for n in nouns_singular if n not in nouns_proper]


nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
nouns_ambiguous = set(nouns_ambiguous)


def categorize_by_template(sentences_in, sentences_out):

    res = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        try:
            start_word = [w for w in s1 if w in start_words][0]
        except IndexError:  # no start word
            raise RuntimeError('Failed to categorize sentence into template')
        else:
            num_adjectives = len(s1[s1.index(start_word) + 1:s1.index('[MASK]')])
            if num_adjectives == 1:  # 1 adjective
                res.setdefault(templates[0], []).append(s2)
            elif num_adjectives == 2:  # 2 adjectives
                res.setdefault(templates[1], []).append(s2)
            elif num_adjectives == 3:  # 3 adjectives
                res.setdefault(templates[2], []).append(s2)

    return res


def categorize_predictions(sentences_out):
    res = {k: 0 for k in prediction_categories}

    # TODO: score correct when start word is plural and predicted ##s turns a preceding word into a plural noun

    for sentence in sentences_out:
        predicted_word = sentence[-2]
        start_word = [w for w in sentence if w in start_words][0]

        # non-start wordpiece
        if predicted_word.startswith("##") or predicted_word == '[UNK]':
            res["non-start\nword-piece\nor\n[UNK]"] += 1

        # proper noun
        if predicted_word in nouns_proper:
            res["noun\nproper"] += 1

        # correct Noun Number
        elif predicted_word in nouns_plural and start_word in start_words_plural:
            res["noun +\ncorrect number"] += 1

        elif predicted_word in nouns_singular and start_word in start_words_singular:
            res["noun +\ncorrect number"] += 1

        # false Noun Number
        elif predicted_word in nouns_plural and start_word in start_words_singular:
            res["noun +\nfalse number"] += 1

        elif predicted_word in nouns_singular and start_word in start_words_plural:
            res["noun +\nfalse number"] += 1

        # Ambiguous Noun
        elif predicted_word in nouns_ambiguous:
            res["noun +\n ambiguous number"] += 1

        # Non_Noun
        else:
            res["non-noun"] += 1

    return res


def print_stats(sentences):

    if not PRINT_STATS:
        return

    num_singular = 0
    num_plural = 0
    num_ambiguous = 0
    num_total = 0
    for s in sentences:
        for w in s:
            if w in nouns_singular:
                num_singular += 1
            elif w in nouns_plural:
                num_plural += 1
            elif w in nouns_ambiguous:
                num_ambiguous += 1
            else:
                raise RuntimeError(f'{w} is neither in plural or singular or ambiguous nouns list')
            num_total += 1
    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')


# score
template2group_name2props = score_predictions(group2predictions_file_paths,
                                              templates,
                                              prediction_categories,
                                              categorize_by_template,
                                              categorize_predictions,
                                              print_stats)
