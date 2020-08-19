from pathlib import Path

from babeval import configs


subjective_copula_singular = ["is", "'s", "was"]  # "do" and "does" should not be considered correct answers
subjective_copula_plural = ["are", "'re", "were"]

templates = ['template1',
             ]

# load word lists
nouns_singular = (Path(__file__).parent / configs.Data.annotator / 'nouns_singular.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / configs.Data.annotator / 'nouns_plural.txt').open().read().split("\n")

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

nouns_singular += ['one', '[NAME]', '[PLACE]', '[MISC]']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)

