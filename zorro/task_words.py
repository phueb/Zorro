from typing import List, Generator, Tuple, Optional
import pandas as pd
from itertools import product
import functools


from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset


def get_task_word_combo(paradigm: str,
                        tag_orders_ns: List[Tuple[str, int, int]],
                        seed: int = configs.Data.seed,
                        verbose: bool = False,
                        ) -> Generator[Tuple, None, None]:

    word_lists = []
    for tag, order, num_in_sample in tag_orders_ns:
        wl = get_task_words(paradigm, tag, order, num_in_sample, seed)
        word_lists.append(wl)
        if verbose:
            print(f'Randomly selected {num_in_sample}/{len(wl)} words with tag ={tag}')
            print(word_lists[-1])
    for combo in product(*word_lists):
        yield combo


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
