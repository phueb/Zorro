from typing import List, Optional
import pandas as pd
import functools
import inflect

from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset


@functools.lru_cache(maxsize=12)
def get_legal_words(tag: str,
                    num_words_in_sample: Optional[int] = None,
                    seed: int = configs.Data.seed,
                    ) -> List[str]:

    print(f'Obtaining words with tag={tag}...')

    # get words with requested tag and order
    df_legal = pd.read_csv(configs.Dirs.legal_words / f'{tag}.csv')
    bool_ids = df_legal['is_legal'].astype(bool).tolist()
    words_legal = df_legal['word'][bool_ids].tolist()

    if num_words_in_sample is None:  # return all possible words, useful for scoring
        return words_legal

    # also counterbalance plural forms
    if tag == 'NN':
        plural = inflect.engine()
        plural_forms = [plural.plural(w) for w in words_legal]
        print(f'Will also counterbalance {len(plural_forms)} plural forms')
    else:
        plural_forms = None

    # find subset of words such that their total corpus frequencies are approx equal across corpora
    res = find_counterbalanced_subset(words_legal,
                                      min_size=num_words_in_sample,
                                      max_size=num_words_in_sample+100,
                                      plural_forms_=plural_forms,
                                      seed=seed,
                                      )

    return res
