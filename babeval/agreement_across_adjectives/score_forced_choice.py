"""
Score predictions made by BERT on agreement across adjectives task.
"""
from pathlib import Path
from typing import List, Tuple

PRINT_STATS = True


pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = ['1 Adjective(s)',
             '2 Adjective(s)',
             # '3 Adjective(s)',
             ]

prediction_categories = ('false', 'correct')

# load word lists
nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split("\n")
nouns_ambiguous = (Path(__file__).parent / 'word_lists' / 'nouns_ambiguous_number_annotator2.txt').open().read().split("\n")

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

# move proper nouns to separate set
nouns_proper = [n for n in nouns_singular if n.istitle()]
nouns_singular = [n for n in nouns_singular if n not in nouns_proper]

# all nouns
nouns = nouns_singular + nouns_plural

# add words
nouns_proper += ['[NAME]', '[PLACE]', '[MISC]']
nouns_singular += ['one']

nouns = set(nouns)
nouns_proper = set(nouns_proper)
nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
nouns_ambiguous = set(nouns_ambiguous)


def categorize_by_template(sentences_in: List[List[str]],
                           cross_entropies: List[float],
                           ):

    template2sentences_in = {}
    template2xes = {}

    for s, xe in zip(sentences_in, cross_entropies):
        try:
            pre_nominal = [w for w in s if w in pre_nominals][0]
        except IndexError:  # no pre-nominal found
            raise RuntimeError('Failed to categorize sentence into template')
        else:
            num_adjectives = len(s[s.index(pre_nominal) + 1:s.index('.') - 1])  # this could be done better
            if num_adjectives == 1:  # 1 adjective
                template2sentences_in.setdefault(templates[0], []).append(s)
                template2xes.setdefault(templates[0], []).append(xe)
            elif num_adjectives == 2:  # 2 adjectives
                template2sentences_in.setdefault(templates[1], []).append(s)
                template2xes.setdefault(templates[1], []).append(xe)
            elif num_adjectives == 3:  # 3 adjectives
                template2sentences_in.setdefault(templates[2], []).append(s)
                template2xes.setdefault(templates[2], []).append(xe)
            else:
                raise ValueError(f'Value of "num_adjectives" ({num_adjectives}) is unexpected.')

    return template2sentences_in, template2xes


def categorize_predictions(sentences_in: List[List[str]],
                           cross_entropies: List[float]):
    """
    for each sentence, an entry in a dict is made, keeping track of:
     1) the cross entropy of the sentence, and
     2) some syntactic phenomenon (e.g. agreement = True or agreement = False).
    When the sentence's alternative choice is detected, the two dict entries are compared.
    When the cross-entropy assigned to the correct choice is higher,
     a value representing "correct" is incremented by one.

    """
    res = {k: 0 for k in prediction_categories}

    def find_target_words(s: List[str]) -> Tuple[str, str, str, str]:
        """
        find two words in sentence which must agree (e.g. "this" and "dog") in single for loop.
        of the three returned objects, only 2 are defined, while the other are of NoneType.
        in theory, this prevents need to search through nouns and pre-nominals again, to determine their number.
        """
        w1s = None
        w1p = None
        w2s = None
        w2p = None
        for w_forward, w_backward in zip(s, reversed(s)):
            if w1s is None and w_forward in pre_nominals_singular:
                w1s = w_forward
            elif w1p is None and w_forward in pre_nominals_plural:
                w1p = w_forward
            if w2s is None and w_backward in nouns_singular:
                w2s = w_backward
            elif w2p is None and w_backward in nouns_plural:
                w2p = w_backward
        return w1s, w1p, w2s, w2p

    noun_s2info = {}  # temporary data structures to speed computation
    noun_p2info = {}

    noun_s_probe = None
    noun_p_probe = None

    for sentence, xe in zip(sentences_in, cross_entropies):
        # get words that either agree or don't, and check if  they do
        pre_nominal_s, pre_nominal_p, noun_s, noun_p = find_target_words(sentence)
        is_agreement = True if (pre_nominal_s and noun_s) or (pre_nominal_p and noun_p) else False

        # add dict entry
        if noun_s:
            noun_s2info[noun_s] = (xe, is_agreement)  # order matters
            noun_s_probe = noun_s
            noun_p_probe = noun_s + 's'
        elif noun_p:
            noun_p2info[noun_p] = (xe, is_agreement)
            noun_s_probe = noun_p[:-1]
            noun_p_probe = noun_p

        # check if match is found
        try:
            tmp = [noun_s2info[noun_s_probe], noun_p2info[noun_p_probe]]  # order matters
        except KeyError:  # match is not found
            continue

        # if match is found, increment "correct" or "false" counter depending on cross-entropy
        else:
            is_correct_s = tmp[0][0] < tmp[1][0] and tmp[0][1]  # xe is lower when pre-nominal and noun are singular
            is_correct_p = tmp[1][0] < tmp[0][0] and tmp[1][1]  # xe is lower when pre-nominal and noun are plural
            if is_correct_s or is_correct_p:  # two ways to be correct
                res["correct"] += 1
            else:
                res["false"] += 1

    print(f'correct={res["correct"]:>9,}')
    print(f'false  ={res["false"]:>9,}')

    return res


def print_stats(sentences):

    if not PRINT_STATS:
        return
