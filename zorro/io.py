from typing import Dict, List, Optional
from pathlib import Path

from zorro import configs


def get_group2model_output_paths(group_names: List[str],
                                 phenomenon: str,
                                 paradigm: str,
                                 step: str = '*',
                                 group_name2step: Optional[Dict[str, int]] = None,
                                 ) -> Dict[str, List[Path]]:
    """
    load files containing the cross entropies assigned to each sentence in the paradigm,
     for all models and steps
     """

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    fn = f'{phenomenon}-{paradigm}'

    # find paths to files, for each group
    res = {}
    for group_name in group_names:

        if group_name2step is not None:
            step = group_name2step[group_name]

        pattern = f'{group_name}/**/saves/{configs.Data.vocab_name}/probing_{fn}_results_{step}.txt'
        model_output_paths = [p for p in runs_path.rglob(pattern)]

        if not model_output_paths:
            raise FileNotFoundError(f'Did not find model output'
                                    f' for group={group_name}'
                                    f' and pattern=probing_{fn}_results_{step}.txt')
        else:
            res[group_name] = model_output_paths

    return res
