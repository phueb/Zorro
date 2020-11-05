from pathlib import Path

from zorro import configs


subjective_copula_singular = ["is", "'s", "was"]  # "do" and "does" should not be considered correct answers
subjective_copula_plural = ["are", "'re", "were"]

templates = ['template1',
             ]

# load task words
task_df = pd.read_csv(configs.Dirs.task_words / f'{Path(__file__).parent.stem}.csv')
nouns_singular = task_df[].tolist()
nouns_plural = task_df[].tolist()

# add words
nouns_singular += ['one']

nouns_plural = set(nouns_plural)
nouns_singular = set(nouns_singular)

