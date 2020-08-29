from typing import Optional, Dict, List
from pathlib import Path

from babeval import configs


def get_group2predictions_file_paths(task_name: str,
                                     task_type: str,
                                     step: int,
                                     ) -> Dict[str, List[Path]]:

    # where to get files from?
    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    # group_names
    if configs.Eval.param_names is None:
        group_names = [p.name for p in runs_path.glob('*')]
    else:
        group_names = configs.Eval.param_names

    # find paths to files, for each group
    group2predictions_file_paths = {}
    for group_name in group_names:
        pattern = '{}/**/saves/{}/probing_{}_results_{}.txt'

        # if requested, find last step
        if step == -1:
            print(f'Finding last step for group={group_name}')
            p = [p for p in sorted(runs_path.rglob(pattern.format(group_name, task_type, task_name, '*')))][-1]
            step = int(p.stem.split('_')[-1])
            print(f'Last step={step}')

        all_paths = [p for p in runs_path.rglob(pattern.format(group_name, task_type, task_name, step))]
        group2predictions_file_paths[group_name] = all_paths[:configs.Eval.max_reps]

    # copy only those groups for which files exist
    res = {}
    for k, v in group2predictions_file_paths.items():
        if not v:
            if configs.Eval.raise_error_on_missing_group:
                raise FileNotFoundError(f'Did not find prediction files for group={k} and step={step}')
            else:
                continue
        else:
            res[k] = v
            print(k)
            print(v)

    return res
