from typing import Optional, List
import pandas as pd

from zorro import configs


def get_vocab_words(ww_name: str = configs.Data.ww_name,
                    tag: Optional[str] = None,
                    ) -> List[str]:
    df = load_vocab_df(ww_name)
    res = []
    for vw, vw_series in df.iterrows():
        vw: str
        if tag is None:
            res.append(vw)
        elif vw_series[tag]:
            res.append(vw)

    return res


def get_frequency(ww_name: str = configs.Data.ww_name,
                  tag: Optional[str] = None,
                  ) -> List[int]:
    ww2info = load_vocab_df(ww_name)
    res = []
    for w, info in ww2info.items():
        if tag in info[1] or tag is None:
            res.append(info[0])


    raise NotImplementedError  # todo return whole word or all vocab words?plementedError  # todo return whole word or all vocab words?

    return res


def load_vocab_df(ww_name: str = configs.Data.ww_name) -> pd.DataFrame:
    path = configs.Dirs.data / 'vocab_words' / f'{ww_name}.csv'
    df = pd.read_csv(path, index_col=0)
    return df

