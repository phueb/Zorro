from typing import List, Generator, Tuple, Optional
import pandas as pd
import random
from itertools import product


from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset


def get_task_word_combo(task_name: str,
                        tag_orders_ns: List[Tuple[str, int, int]],
                        seed: int = configs.Data.seed,
                        verbose: bool = False,
                        ) -> Generator[Tuple, None, None]:

    word_lists = []
    for tag, order, ns in tag_orders_ns:
        wl = get_task_words(task_name, tag, order, ns, seed)
        word_lists.append(wl)
        if verbose:
            print(f'Randomly selected {ns}/{len(wl)} words with tag ={tag}')
            print(word_lists[-1])

    for combo in product(*word_lists):
        yield combo


def get_task_words(task_name: str,
                   tag: str,
                   order: int = 0,
                   num_words_in_sample: Optional[int] = None,
                   seed: int = configs.Data.seed,
                   ) -> List[str]:

    # get words with requested tag and order
    task_df = pd.read_csv(configs.Dirs.task_words / f'{task_name}.csv')
    bool_ids = task_df[f'{tag}-{order}'].astype(bool).tolist()
    task_words = task_df['word'][bool_ids].tolist()

    if num_words_in_sample is None:  # return all possible words, useful for scoring
        return task_words

    # find subset of task words such that their total corpus frequencies are approx equal across corpora
    res = find_counterbalanced_subset(task_words,
                                      min_size=num_words_in_sample-20,
                                      max_size=num_words_in_sample+20,
                                      seed=seed,
                                      )
    return res
