from pathlib import Path
import pandas as pd

from babeval import configs

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = ['template1',
             ]

# load task words
task_df = pd.read_csv(configs.Dirs.task_words / f'{Path(__file__).parent.stem}.csv')
nouns_singular = task_df['NN'].tolist()
nouns_plural = task_df['NNS'].tolist()
# external
nouns_ambiguous = (configs.Dirs.external_words / 'nouns_ambiguous_number.txt').open().read().split("\n")
nouns_proper = (configs.Dirs.external_words / 'nouns_proper.txt').open().read().split("\n")

# add words
nouns_singular += ['one']

nouns_proper = set(nouns_proper)
nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
nouns_ambiguous = set(nouns_ambiguous)

