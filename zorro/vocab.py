from typing import Optional, List
import pandas as pd
import functools

from zorro import configs


@functools.lru_cache(maxsize=12)
def get_vocab_words(vocab_name: Optional[str] = None,
                    tag: Optional[str] = None,
                    return_excluded_words: bool = False,  # sub-words, stop-words, number-words
                    ) -> List[str]:

    if vocab_name is None:
        vocab_name = configs.Data.vocab_name_template.format(configs.Data.vocab_size)

    df = load_vocab_df(vocab_name, return_excluded_words)
    res = []
    for vw, vw_series in df.iterrows():
        vw: str
        if tag is None or vw_series[tag]:
            res.append(vw)

    return res


def get_frequency(vocab_name: Optional[str] = None,
                  tag: Optional[str] = None,
                  corpus_initial: Optional[str] = 'total',
                  return_excluded_words: bool = False,
                  ) -> List[int]:

    if vocab_name is None:
        vocab_name = configs.Data.vocab_name_template.format(configs.Data.vocab_size)

    df = load_vocab_df(vocab_name, return_excluded_words)
    res = []
    for vw, vw_series in df.iterrows():
        vw: str
        if tag is None or vw_series[tag]:
            f = vw_series[f'{corpus_initial}-frequency']
            res.append(f)

    return res


def load_vocab_df(vocab_name: Optional[str] = None,
                  return_excluded_words: bool = False,
                  ) -> pd.DataFrame:

    if vocab_name is None:
        vocab_name = configs.Data.vocab_name_template.format(configs.Data.vocab_size)

    path = configs.Dirs.data / 'vocab_words' / f'{vocab_name}.csv'
    df = pd.read_csv(path, index_col=0, na_filter=False, dtype={'is_excluded': bool})

    if return_excluded_words:
        res = df
    else:
        res = df[df['is_excluded'] == False]

    return res
