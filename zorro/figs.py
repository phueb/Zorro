import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Union, Optional
import yaml

from matplotlib import rcParams

from zorro import configs

rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False


def shorten_tick_labels(labels: List[Union[str,int]],
                        ) -> List[str]:
    return [str(label)[:-3] + 'K' if str(label).endswith('000') else label
            for label in labels]


def get_legend_label(group_name,
                     reps,
                     conditions: Optional[List[str]] = None,
                     add_group_name: bool = False,
                     ) -> str:
    if group_name.endswith('frequency baseline'):
        return 'frequency baseline'

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    param2val = load_param2val(group_name, runs_path)

    if group_name.startswith('param'):
        model_name = 'BabyBERTa'
    else:
        model_name = 'RoBERTa-base'
        conditions = ['corpora']

    # make label
    res = f'{model_name} | n={reps} | '
    for c in conditions or configs.Eval.conditions:
        if c == 'load_from_checkpoint' and param2val[c] != 'none':
            param2val_previous = load_param2val(param2val[c], runs_path)
            res += f'previously trained on={param2val_previous["corpora"]} '
            continue
        try:
            val = param2val[c]
        except KeyError:
            if c == 'corpora':
                val = 'Liu et al., 2019'
            else:
                val = 'n/a'
        if isinstance(val, bool):
            val = int(val)
        res += f'{c}={val} '

    if add_group_name:
        res += ' | ' + group_name

    return res


def load_param2val(group_name, runs_path):
    path = runs_path / group_name / 'param2val.yaml'
    with path.open('r') as f:
        param2val = yaml.load(f, Loader=yaml.FullLoader)
    return param2val
