from pathlib import Path

from babeval import configs

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = [
    'Look at ...',
    '... went there',
             ]

# load word lists
adjectives = (Path(__file__).parent / configs.Data.annotator / 'adjectives.txt').open().read().split("\n")
nouns_singular = (Path(__file__).parent / configs.Data.annotator / 'nouns_singular.txt').open().read().split("\n")
nouns_plural = (Path(__file__).parent / configs.Data.annotator / 'nouns_plural.txt').open().read().split("\n")
nouns_ambiguous = (Path(__file__).parent / configs.Data.annotator / 'nouns_ambiguous_number.txt').open().read().split("\n")

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

# make sure no title-cased words are in nouns
assert not [n for n in nouns_singular if n.istitle()]

# new nouns lists
nouns = nouns_singular + nouns_plural
nouns_proper = ['[NAME]', '[PLACE]', '[MISC]']

# add words
nouns_singular += ['one']

nouns = set(nouns)
nouns_proper = set(nouns_proper)
nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
nouns_ambiguous = set(nouns_ambiguous)