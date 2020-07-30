"""
Score predictions made by BERT on agreement_across_adjectives_2 task.

ex: look at [MASK] fighting toy .
replace [MASK] with start_word .

"""
from pathlib import Path
from typing import List

PRINT_STATS = False

# load word lists
nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split("\n")
nouns_ambiguous = (Path(__file__).parent / 'word_lists' / 'nouns_ambiguous_number_annotator2.txt').open().read().split("\n")
nouns_lst = (Path(__file__).parent / 'word_lists' / 'nouns_annotator2.txt').open().read().split("\n")

templates = ['1 Adjective(s)',
             '2 Adjective(s)',
             '3 Adjective(s)',
             ]

prediction_categories = (
    "start_word +\ncorrect number",
    "start_word +\nfalse number",
    "noun +\n ambiguous number", #does not count agreement between start_word and ambiguous nouns
    "non-start\nword-piece\nor\n[UNK]",
    "non-start_word",
)

start_words_singular = ["this", "that"]
start_words_plural = ["these", "those"]
start_words = set(start_words_singular + start_words_plural)

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


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        try:
            noun = [w for w in s1 if w in nouns_lst][0] #TODO: this may not be working when adjectives also appear in nouns_lst
        except IndexError:  # no noun
            raise RuntimeError('Failed to categorize sentence into template')
        else:

            # num_adjectives: the number of words in between [MASK] and noun

            num_adjectives = len(s1[s1.index('[MASK]')+1:s1.index(noun)])
            if num_adjectives == 1:  # 1 adjective
                template2sentences_out.setdefault(templates[0], []).append(s2)
                if templates[0] not in template2mask_index:
                    template2mask_index[templates[0]] = s1.index('[MASK]')
            elif num_adjectives == 2:  # 2 adjectives
                template2sentences_out.setdefault(templates[1], []).append(s2)
                if templates[1] not in template2mask_index:
                    template2mask_index[templates[1]] = s1.index('[MASK]')
            elif num_adjectives == 3:  # 3 adjectives
                template2sentences_out.setdefault(templates[2], []).append(s2)
                if templates[2] not in template2mask_index:
                    template2mask_index[templates[2]] = s1.index('[MASK]')

    return template2sentences_out, template2mask_index

def categorize_predictions(sentences_out: List[List[str]], mask_index: int):
    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        noun = [w for w in sentence if w in nouns_lst][0]

        # non-start wordpiece
        if predicted_word.startswith("##") or predicted_word == '[UNK]':
            if predicted_word != '##s':
                res["non-start\nword-piece\nor\n[UNK]"] += 1

        # correct start_word
        if predicted_word in start_words_plural and noun in nouns_plural:
            res["start_word +\ncorrect number"] += 1

        elif predicted_word in start_words_singular and noun in nouns_singular:
            res["start_word +\ncorrect number"] += 1

        # false start_word
        elif predicted_word in start_words_plural and noun in nouns_singular:
            res["start_word +\nfalse number"] += 1

        elif predicted_word in start_words_singular and noun in nouns_plural:
            res["start_word +\nfalse number"] += 1

        # Ambiguous Noun:
        # when the noun is in nouns_ambiguous, does not count the its agreement with start_word
        elif noun in nouns_ambiguous:
            res["noun +\n ambiguous number"] += 1

        # Non_start_word
        else:
            res["non-start_word"] += 1

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
            if w in start_words_singular:
                num_singular += 1
            elif w in start_words_plural:
                num_plural += 1
            # elif w in nouns_ambiguous:
            #     num_ambiguous += 1
            else:
                raise RuntimeError(f'{w} is neither in plural or singular start_words list')
            num_total += 1

    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')



