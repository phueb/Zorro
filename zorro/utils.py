from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from pathlib import Path

from zorro.scoring import count_correct_choices
from zorro.data import DataExperimental
from zorro import configs


def get_reps(model_output_paths: List[Path],
             step: Union[int, None],
             ) -> int:
    if step is not None:
        pattern = f'_{step}'
    else:
        pattern = ''
    return len([path for path in model_output_paths if path.stem.endswith(pattern)])


def prepare_data_for_plotting(gn2model_output_paths: Dict[str, List[Path]],
                              phenomenon: str,
                              paradigm: str,
                              ) -> Dict[str, Dict[str, np.array]]:
    """
    :param gn2model_output_paths: dict mapping group name to paths of files containing predictions at a specific step
    :param phenomenon: name of phenomenon
    :param paradigm: name of paradigm
    :return: double-embedded dict, which can be input to barplot function

    how it works: for each group of model output:
    1. the model output are read and categorized by template (or not)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    this functions scores all model output associated with a single paradigm,
    and produces all results necessary to plot a single figure.

    'accuracies' is a vector containing accuracies, one per replication
    """

    if not configs.Eval.categorize_by_template:
        templates = ['all templates']
    else:
        raise NotImplementedError  # TODO read template info directly from local text files containing sentences

    group_names = list(gn2model_output_paths.keys())

    # init result: a vector populated with accuracies, one for each model rep, per group, per template
    res = {template: {gn: np.zeros(len(output_paths)) for gn, output_paths in gn2model_output_paths.items()}
           for template in templates}

    for group_name in group_names:

        # read model output into instance of DataExperimental
        output_paths = gn2model_output_paths[group_name]
        if not output_paths:
            print(f'Did not find model output files. Consider reducing max step. Skipping')
            continue
        data_instances = [DataExperimental(op, phenomenon, paradigm) for op in output_paths]

        for row_id, data in enumerate(data_instances):

            # organize sentence pairs by template
            if configs.Eval.categorize_by_template:
                raise NotImplementedError
            else:
                template2pairs = {templates[0]: data.pairs}

            for template in templates:

                pairs = template2pairs[template]
                assert pairs

                # calc proportion correct - sentences on odd lines are bad, and sentences on even lines are good
                num_correct = count_correct_choices(data)
                accuracy = num_correct / len(pairs)

                # populate vector of proportions - one vector per model group
                res[template][group_name][row_id] = accuracy

    return res


def get_phenomena_and_paradigms(excluded_paradigms: Optional[List[str]] = None,
                                ) -> List[Tuple[str, str]]:
    phenomena = [
        'npi_licensing',
        'ellipsis',
        'filler-gap',
        'case',
        'argument_structure',
        'local_attractor',
        'agreement_subject_verb',
        'agreement_demonstrative_subject',
        'irregular_verb',
        'island-effects',
        'quantifiers',
    ]

    if not excluded_paradigms:
        excluded_paradigms = configs.Eval.excluded_paradigms

    # get list of (phenomenon, paradigm) tuples
    res = []
    for phenomenon in phenomena:
        for p in (configs.Dirs.src / phenomenon).glob('*.py'):
            paradigm = p.stem
            if paradigm in excluded_paradigms:
                continue
            res.append((phenomenon, paradigm))

    return res


def filter_by_step(model_output_path: Path,
                   step: int,
                   ) -> bool:
    if int(model_output_path.stem.split('_')[-1]) == step:
        return True
    return False
