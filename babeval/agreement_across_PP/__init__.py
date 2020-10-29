from pathlib import Path

from babeval import configs

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

templates = [
    'template1',
             ]

nouns_plural = (configs.Dirs.task_words / Path(__file__).stem / 'nouns_plural.txt').open().read().split()
nouns_singular = (configs.Dirs.task_words / f'{Path(__file__).stem}.csv').open().read().split()
prepositions = (configs.Dirs.task_words / Path(__file__).stem / 'prepositions.txt').open().read().split()
adjectives = (configs.Dirs.task_words / Path(__file__).stem / 'adjectives.txt').open().read().split()

# add words
nouns_singular += ['one']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
