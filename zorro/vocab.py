from typing import Optional, List, Dict, Tuple
from collections import OrderedDict

from zorro import configs


def get_whole_words(ww_name: str = configs.Data.ww_name,
                    tag: Optional[str] = None,
                    ) -> List[str]:
    ww2info = get_ww2info(ww_name)
    res = []
    for w, info in ww2info.items():
        if tag in info[1] or tag is None:
            res.append(w)

    raise NotImplementedError  # todo return whole word or all vocab words?plementedError  # todo return whole word or all vocab words?
    return res


def get_frequency(ww_name: str = configs.Data.ww_name,
                    tag: Optional[str] = None,
                    ) -> List[int]:
    ww2info = get_ww2info(ww_name)
    res = []
    for w, info in ww2info.items():
        if tag in info[1] or tag is None:
            res.append(info[0])


    raise NotImplementedError  # todo return whole word or all vocab words?plementedError  # todo return whole word or all vocab words?

    return res


def get_ww2info(ww_name: str = configs.Data.ww_name) -> Dict[str, Tuple[int, List[str]]]:
    lines = (configs.Dirs.data / 'vocab_words' / f'{ww_name}.txt').open().read().split("\n")
    res = OrderedDict()
    for line in lines:
        if line == '':
            continue  # last line
        w, f = line.split()[:2]
        tags = line.split()[2:]
        res[w] = (int(f), tags)

    raise NotImplementedError  # todo return whole word or all vocab words?
    return res

