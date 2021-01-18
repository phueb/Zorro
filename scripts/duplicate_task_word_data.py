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