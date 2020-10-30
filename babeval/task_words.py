from typing import List, Generator, Tuple
import pandas as pd
import random
from itertools import product


from babeval import configs


def get_task_word_combo(task_name: str,
                        tag_orders_ns,
                        seed: int = configs.Data.seed,
                        ) -> Generator[Tuple, None, None]:
    random.seed(seed)

    word_lists = []
    for tag, order, ns in tag_orders_ns:
        wl = get_task_words(task_name, tag, order)
        print(f'Selecting {ns}/{len(wl)} words with tag ={tag}')
        word_lists.append(random.sample(wl, k=ns))

    for combo in product(*word_lists):
        yield combo


def get_task_words(task_name: str,
                   tag: str,
                   order: int = 0,
                   ) -> List[str]:
    task_df = pd.read_csv(configs.Dirs.task_words / f'{task_name}.csv')
    bool_ids = task_df[f'{tag}-{order}'].astype(bool).tolist()
    res = task_df['word'][bool_ids].tolist()
    return res
