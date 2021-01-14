from typing import Optional, Dict, List
from pathlib import Path

from zorro import configs


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
        group_names = sorted([p.name for p in runs_path.glob('*')])
    else:
        group_names = configs.Eval.param_names

    get_step = lambda s: int(s) if s.isdigit() else s

    # find paths to files, for each group
    group2predictions_file_paths = {}
    for group_name in group_names:
        pattern = '{}/**/saves/{}/probing_{}_results_{}.txt'

        # if requested, find last step
        if step == -1:
            print(f'Finding last step for group={group_name}...')
            steps = [get_step(p.stem.split('_')[-1])
                     for p in runs_path.rglob(pattern.format(group_name, task_type, task_name, '*'))]

            if configs.Eval.raise_error_on_missing_group and not steps:
                raise FileNotFoundError(f'Did not find prediction files for group={group_name}')

            if isinstance(steps[0], str):
                effective_step = list(sorted(steps))[0]  # sorts "best" before "last"
                print(f'Found step={effective_step}')
            else:
                effective_step = max(steps)
                print(f'Found last step={effective_step:,}')
        else:
            effective_step = step

        all_paths = [p for p in runs_path.rglob(pattern.format(group_name, task_type, task_name, effective_step))]
        group2predictions_file_paths[group_name] = all_paths[:configs.Eval.max_reps]

    # copy only those groups for which files exist
    res = {}
    for k, v in group2predictions_file_paths.items():
        if not v:
            if configs.Eval.raise_error_on_missing_group:
                raise FileNotFoundError(f'Did not find prediction files for group={k} and step={step}')
        else:
            res[k] = v
            print(k)
            print(v)

    return res
