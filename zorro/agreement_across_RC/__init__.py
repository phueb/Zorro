from pathlib import Path

from zorro import configs

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

pronouns_1p_2p = ['i', 'you', 'we']
pronouns_3p = ['he', 'she', 'it']
assert len(pronouns_3p) == len(pronouns_1p_2p)

templates = [
    'object-relative',
    'subject-relative',
]

nouns_plural = (configs.Dirs.task_words / Path(__file__).stem / 'nouns_plural.txt').open().read().split()
nouns_singular = (configs.Dirs.task_words / f'{Path(__file__).stem}.csv').open().read().split()
adjectives = (configs.Dirs.task_words / Path(__file__).stem / 'adjectives.txt').open().read().split()

# add words
nouns_singular += ['one']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
