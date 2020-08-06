"""
Score predictions made by BERT on agreement_across_adjectives_2 task.

ex: look at [MASK] fighting toy .
replace [MASK] with demonstrative .

"""
from pathlib import Path
from typing import List

PRINT_STATS = False

# load word lists
nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split("\n")
nouns = (Path(__file__).parent / 'word_lists' / 'nouns_annotator2.txt').open().read().split("\n")

templates = ['1 Adjective(s)',
             '2 Adjective(s)',
             '3 Adjective(s)',
             ]

prediction_categories = (
    "demonstrative +\ncorrect number",
    "demonstrative +\nfalse number",
    "article +\nambiguous number",
    "non-start\nword-piece\nor\n[UNK]",
    "other",
)

demonstratives_singular = ["this", "that"]
demonstratives_plural = ["these", "those"]
demonstratives_ambiguous = ['the']

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular


# move proper nouns to separate set
nouns_proper = [n for n in nouns_singular if n.istitle()]
nouns_singular = [n for n in nouns_singular if n not in nouns_proper]

# add words
nouns_proper += ['[NAME]', '[PLACE]', '[MISC]']
nouns_singular += ['one']

nouns_proper = set(nouns_proper)
nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)


def categorize_by_template(sentences_in, sentences_out: List[List[str]]):

    template2sentences_out = {}
    template2mask_index = {}
    for s1, s2 in zip(sentences_in, sentences_out):
        # num_adjectives: the number of words in between [MASK] and noun
        num_adjectives = len(s1[s1.index('[MASK]')+1:s1.index('.')-1])
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
        else:
            raise RuntimeError('Failed to categorize sentence into template')

    return template2sentences_out, template2mask_index


def categorize_predictions(sentences_out: List[List[str]], mask_index: int):
    res = {k: 0 for k in prediction_categories}

    for sentence in sentences_out:
        predicted_word = sentence[mask_index]
        noun = sentence[-2]  # use positional indexing because there is overlap between adjectives and nouns

        # non-start wordpiece
        if predicted_word.startswith("##") or predicted_word == '[UNK]':
            if predicted_word != '##s':
                res["non-start\nword-piece\nor\n[UNK]"] += 1

        # correct demonstrative
        if predicted_word in demonstratives_plural and noun in nouns_plural:
            res["demonstrative +\ncorrect number"] += 1

        elif predicted_word in demonstratives_singular and noun in nouns_singular:
            res["demonstrative +\ncorrect number"] += 1

        # false demonstrative
        elif predicted_word in demonstratives_plural and noun in nouns_singular:
            res["demonstrative +\nfalse number"] += 1

        elif predicted_word in demonstratives_singular and noun in nouns_plural:
            res["demonstrative +\nfalse number"] += 1

        # Ambiguous
        elif predicted_word in demonstratives_ambiguous:
            res["article +\nambiguous number"] += 1

        # Non_demonstrative
        else:
            res["other"] += 1

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
            if w in demonstratives_singular:
                num_singular += 1
            elif w in demonstratives_plural:
                num_plural += 1
            # elif w in nouns_ambiguous:
            #     num_ambiguous += 1
            else:
                raise RuntimeError(f'{w} is neither in plural or singular demonstratives list')
            num_total += 1

    print(f'Sing: {num_singular / num_total:.2f} Plural: {num_plural / num_total:.2f}')



