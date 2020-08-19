from pathlib import Path

from babeval import configs

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

pronouns_1p_2p = ['I', 'you', 'we']
pronouns_3p = ['he', 'she', 'it']
assert len(pronouns_3p) == len(pronouns_1p_2p)

templates = [
    'object-relative',
    'subject-relative',
]

nouns_plural = (Path(__file__).parent / configs.Data.annotator / 'nouns_plural.txt').open().read().split()
nouns_singular = (Path(__file__).parent / configs.Data.annotator / 'nouns_singular.txt').open().read().split()
adjectives = (Path(__file__).parent / configs.Data.annotator / 'adjectives.txt').open().read().split()

# check for list overlap
for w in nouns_singular:
    assert w not in nouns_plural
for w in nouns_plural:
    assert w not in nouns_singular

nouns_singular += ['one', '[NAME]', '[PLACE]', '[MISC]']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)


