from typing import Dict, List
from pathlib import Path

from zorro import configs


def get_group2model_output_paths(group_names: List[str],
                                 runs_path: Path,
                                 phenomenon: str,
                                 paradigm: str,
                                 step: str = '*',
                                 ) -> Dict[str, List[Path]]:
    """load files containing the cross entropies assigned to each sentence in the paradigm, for all models and steps"""

    fn = f'{phenomenon}-{paradigm}'

    # find paths to files, for each group
    res = {}
    for group_name in group_names:
        print(f'Looking for prediction files for {group_name}')

        pattern = f'{group_name}/**/saves/forced_choice/**/probing_{fn}_results_{step}.txt'
        model_output_paths = [p for p in runs_path.rglob(pattern)]

        if not model_output_paths:
            raise FileNotFoundError(f'Did not find model output'
                                    f' for group={group_name}'
                                    f' and vocab size={configs.Data.vocab_size}'
                                    f' and pattern=probing_{fn}_results_{step}.txt')
        else:
            res[group_name] = model_output_paths

    return res
