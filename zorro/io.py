from typing import Dict, List
from pathlib import Path

from zorro import configs


def get_group2predictions_file_paths(group_names: List[str],
                                     runs_path: Path,
                                     phenomenon: str,
                                     paradigm: str,
                                     ) -> Dict[str, List[Path]]:
    """load files containing the cross entropies assigned to each sentence in the paradigm, for all models and steps"""

    fn = f'{phenomenon}-{paradigm}'

    # find paths to files, for each group
    res = {}
    for group_name in group_names:
        pattern = '{}/**/saves/forced_choice/**/probing_{}_results_*.txt'
        prediction_file_paths = [p for p in runs_path.rglob(pattern.format(group_name, fn))]

        if not prediction_file_paths:
            raise FileNotFoundError(f'Did not find prediction files'
                                    f' for group={group_name}'
                                    f' and vocab size={configs.Data.vocab_size}'
                                    f' and pattern=probing_{fn}_results_*.txt')
        else:
            res[group_name] = prediction_file_paths
            print(group_name)
            print(prediction_file_paths)

    return res
