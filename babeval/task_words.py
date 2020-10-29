import pandas as pd
import random
from itertools import product


from babeval import configs


def get_task_word_combo(task_name: str,
                        tag_orders_ns,
                        ):
    random.seed(configs.Data.seed)

    task_df = pd.read_csv(configs.Dirs.task_words / f'{task_name}.csv')

    word_lists = []
    for tag, order, ns in tag_orders_ns:
        bool_ids = task_df[f'{tag}-{order}'].astype(bool).tolist()
        wl = task_df['word'][bool_ids].tolist()
        print(f'Selecting {ns}/{len(wl)} words with tag ={tag}')
        word_lists.append(random.sample(wl, k=ns))

    for combo in product(*word_lists):
        yield combo
