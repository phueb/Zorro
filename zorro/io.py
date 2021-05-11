from typing import Dict, List
from pathlib import Path

from zorro import configs


def get_group2predictions_file_paths(group_names: List[str],
                                     runs_path: Path,
                                     paradigm: str,
                                     ) -> Dict[str, List[Path]]:

    # find paths to files, for each group
    group2predictions_file_paths = {}
    for group_name in group_names:
        pattern = '{}/**/saves/{}/**/probing_{}_results_*.txt'
        group2predictions_file_paths[group_name] = [p for p in runs_path.rglob(pattern.format(group_name,
                                                                                              'forced_choice',
                                                                                              paradigm))]

    # copy only those groups for which files exist
    res = {}
    for k, v in group2predictions_file_paths.items():
        if not v:
            if configs.Eval.raise_error_on_missing_group:
                raise FileNotFoundError(f'Did not find prediction files'
                                        f' for group={k} and vocab size={configs.Data.vocab_size}')
        else:
            res[k] = v
            print(k)
            print(v)

    return res
