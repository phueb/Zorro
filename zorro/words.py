from typing import List, Optional
import pandas as pd
import functools


from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset


@functools.lru_cache(maxsize=12)
def get_words_for_paradigm(paradigm: str,
                           tag: str,
                           order: int = 0,
                           num_words_in_sample: Optional[int] = None,
                           seed: int = configs.Data.seed,
                           ) -> List[str]:

    print(f'Obtaining words with tag={tag}...')

    # get words with requested tag and order
    df_paradigm = pd.read_csv(configs.Dirs.words_in_paradigm / f'{paradigm}.csv')
    bool_ids = df_paradigm[f'{tag}-{order}'].astype(bool).tolist()
    words_in_slot = df_paradigm['word'][bool_ids].tolist()

    if num_words_in_sample is None:  # return all possible words, useful for scoring
        return words_in_slot

    # find subset of words such that their total corpus frequencies are approx equal across corpora
    res = find_counterbalanced_subset(words_in_slot,
                                      min_size=num_words_in_sample,
                                      max_size=num_words_in_sample+100,
                                      seed=seed,
                                      )

    # exclude accidental plural nouns
    if tag == 'NN':
        try:
            res.remove('people')
        except ValueError:
            pass

    return res