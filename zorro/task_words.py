from typing import List, Optional
import pandas as pd
import functools


from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset


@functools.lru_cache(maxsize=12)
def get_task_words(paradigm: str,
                   tag: str,
                   order: int = 0,
                   num_words_in_sample: Optional[int] = None,
                   seed: int = configs.Data.seed,
                   ) -> List[str]:

    print(f'Obtaining task words with tag={tag}...')

    # get words with requested tag and order
    task_df = pd.read_csv(configs.Dirs.task_words / f'{paradigm}.csv')
    bool_ids = task_df[f'{tag}-{order}'].astype(bool).tolist()
    task_words = task_df['word'][bool_ids].tolist()

    if num_words_in_sample is None:  # return all possible words, useful for scoring
        return task_words

    # find subset of task words such that their total corpus frequencies are approx equal across corpora
    res = find_counterbalanced_subset(task_words,
                                      min_size=num_words_in_sample,
                                      max_size=num_words_in_sample+100,
                                      seed=seed,
                                      )
    return res
