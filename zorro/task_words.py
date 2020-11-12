from typing import List, Generator, Tuple
import pandas as pd
import random
from itertools import product
import numpy as np


from zorro import configs


def get_task_word_combo(task_name: str,
                        tag_orders_ns: List[Tuple[str, int, int]],
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
                   fdt: int = configs.Data.frequency_difference_tolerance,
                   verbose_warn: bool = False,
                   ) -> List[str]:

    # get words with requested tag and order
    task_df = pd.read_csv(configs.Dirs.task_words / f'{task_name}.csv')
    bool_ids = task_df[f'{tag}-{order}'].astype(bool).tolist()
    task_words = task_df['word'][bool_ids].tolist()

    from zorro.vocab import load_vocab_df

    vocab_df = load_vocab_df()
    f_df = vocab_df.filter(regex='^.-frequency', axis=1)
    vw2fs = {w: fs.values for w, fs in f_df.iterrows()}

    # subsample words which occur roughly equally across corpora
    res = []
    corpus_fs_list = []
    for tw in task_words:
        corpus_fs = vw2fs[tw]
        mean_f = np.mean(corpus_fs)
        if all([mean_f - fdt < f < mean_f + fdt for f in corpus_fs]):
            res.append(tw)
            corpus_fs_list.append(corpus_fs)
            print(f'Including "{tw:<24}"', corpus_fs)
        elif verbose_warn:
            print(f'WARNING: Excluding "{tw:<24}" due to very different corpus frequencies.', corpus_fs)

    if not res:
        raise RuntimeError(f'No task words available for {task_name}.'
                           f' Is frequency_difference_tolerance too small?')

    # check overall bias in corpus frequency
    for name, f in zip(f_df.columns, np.array(corpus_fs_list).mean(axis=0)):
        print(f'{name:<24} mean={f:>9.2f}')

    return res
