from pathlib import Path

from zorro import configs

subjective_copula_singular = ["does"]  # only "do" and does should be considered answers
subjective_copula_plural = ["do"]
subjective_copula_ambiguous = ["did"]

templates = ['template1',
             ]

# load task words
task_df = pd.read_csv(configs.Dirs.task_words / f'{Path(__file__).parent.stem}.csv')
nouns_plural = (configs.Dirs.task_words / Path(__file__).stem / 'nouns_plural.txt').open().read().split()
nouns_singular = (configs.Dirs.task_words / f'{Path(__file__).stem}.csv').open().read().split()

# add words
nouns_singular += ['one']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)

