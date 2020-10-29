from pathlib import Path

from babeval import configs

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = [
    'look at ...',
    '... went there',
             ]

# load task words
task_df = pd.read_csv(configs.Dirs.task_words / f'{Path(__file__).parent.stem}.csv')
adjectives = (configs.Dirs.task_words / Path(__file__).stem / 'adjectives.txt').open().read().split("\n")
nouns_singular = task_df[].tolist()
nouns_plural = task_df[].tolist()

# external
nouns_ambiguous = task_df[].tolist()
nouns_proper = task_df[].tolist()

# add words
nouns_singular += ['one']

nouns_proper = set(nouns_proper)
nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)
nouns_ambiguous = set(nouns_ambiguous)