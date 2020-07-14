from typing import Optional, Dict, List
from pathlib import Path

from babeval import configs


def get_group2predictions_file_paths(task_name: str,
                                     step: Optional[int] = None,
                                     ) -> Dict[str, List[Path]]:
    if step is None:
        step = configs.Eval.step

    # get prediction file paths from this repository (dummies)
    if configs.Eval.dummy:
        runs_path = configs.Dirs.dummy_predictions
    # get prediction file paths from lab server
    else:
        runs_path = configs.Dirs.predictions

    group2pattern = {g: f'{g}/**/saves/probing_{task_name}_results_{step}.txt'
                     for g in configs.Eval.param_names}
    print(group2pattern)
    group2predictions_file_paths = {g: [p for p in runs_path.rglob(pattern)][:configs.Eval.max_reps]
                                    for g, pattern in group2pattern.items()}

    # check paths
    for k, v in group2predictions_file_paths.items():
        assert v, f'Did not find prediction files for group ={k}'
        print(k)
        print(v)

    return group2predictions_file_paths
