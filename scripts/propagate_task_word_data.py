"""
use to copy data in agreement_across_1_adjective.csv to other task word csv files,
 to save time entering redundant data manually into each
"""
import pandas as pd

from zorro import configs

src_path = configs.Dirs.task_words / 'agreement_across_1_adjective.csv'
src_df = pd.read_csv(src_path)

dst1_df = src_df.copy()
dst1_df['JJ-1'] = dst1_df['JJ-0']
dst1_path = configs.Dirs.task_words / 'agreement_across_2_adjectives.csv'
dst1_df.to_csv(dst1_path, index=False)

dst2_df = src_df.copy()
dst2_path = configs.Dirs.task_words / 'agreement_across_RC.csv'
dst2_df.to_csv(dst2_path, index=False)

dst3_df = src_df.copy()
dst3_df['NN-1'] = dst3_df['NN-0']
dst3_path = configs.Dirs.task_words / 'agreement_across_PP.csv'
dst3_df.to_csv(dst3_path, index=False)

dst4_df = src_df.copy()
dst3_path = configs.Dirs.task_words / 'agreement_between_neighbors.csv'
dst4_path = configs.Dirs.task_words / 'agreement_in_1_verb_question.csv'
dst5_path = configs.Dirs.task_words / 'agreement_in_2_verb_question.csv'
dst4_df.to_csv(dst3_path, index=False)
dst4_df.to_csv(dst4_path, index=False)
dst4_df.to_csv(dst5_path, index=False)

dst5_df = src_df.copy()
dst5_path = configs.Dirs.task_words / 'irregular_past_participle_verb_intransitive.csv'
dst5_df.to_csv(dst5_path, index=False)