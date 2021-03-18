from typing import Optional, List
import pandas as pd

from zorro import configs


def get_vocab_words(vocab_name: str = configs.Data.vocab_name,
                    tag: Optional[str] = None,
                    ) -> List[str]:
    df = load_vocab_df(vocab_name)
    res = []
    for vw, vw_series in df.iterrows():
        vw: str
        if tag is None or vw_series[tag]:
            res.append(vw)

    return res


def get_frequency(vocab_name: str = configs.Data.vocab_name,
                  tag: Optional[str] = None,
                  corpus_initial: Optional[str] = 'total',
                  ) -> List[int]:
    df = load_vocab_df(vocab_name)
    res = []
    for vw, vw_series in df.iterrows():
        vw: str
        if tag is None or vw_series[tag]:
            f = vw_series[f'{corpus_initial}-frequency']
            res.append(f)

    return res


def load_vocab_df(vocab_name: str = configs.Data.vocab_name) -> pd.DataFrame:
    path = configs.Dirs.data / 'vocab_words' / f'{vocab_name}.csv'
    df = pd.read_csv(path, index_col=0, na_filter=False)
    return df

