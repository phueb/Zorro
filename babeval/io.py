from typing import Optional, Dict, List
from pathlib import Path

from babeval import configs


def get_group2predictions_file_paths(task_name: str,
                                     task_type: str,
                                     step: int,
                                     ) -> Dict[str, List[Path]]:

    # get prediction file paths from local machine (faster read-times)
    if configs.Eval.dummy:
        runs_path = configs.Dirs.runs_local
    # get prediction file paths from lab server
    else:
        runs_path = configs.Dirs.runs_server

    group2pattern = {g: f'{g}/**/saves/{task_type}/probing_{task_name}_results_{step}.txt'
                     for g in configs.Eval.param_names}
    print(group2pattern)
    group2predictions_file_paths = {g: [p for p in runs_path.rglob(pattern)][:configs.Eval.max_reps]
                                    for g, pattern in group2pattern.items()}

    # copy only those groups for which files exist
    res = {}
    for k, v in group2predictions_file_paths.items():
        if not v:
            if configs.Eval.raise_error_on_missing_group:
                raise FileNotFoundError(f'Did not find prediction files for group={k}')
            else:
                continue
        else:
            res[k] = v
            print(k)
            print(v)

    return res
