from typing import Dict, List, Tuple
import numpy as np
from pathlib import Path

from zorro.scoring import count_correct_choices
from zorro.data import DataExperimental, DataControl
from zorro import configs


def prepare_data_for_plotting(group2predictions_file_paths: Dict[str, List[Path]],
                              phenomenon: str,
                              paradigm: str,
                              ) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param phenomenon: name of phenomenon
    :param paradigm: name of paradigm
    :return: double-embedded dict, which can be input to barplot function

    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template (or not)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    Multiple frequency-control groups are added.

    this functions scores all prediction files associated with a single paradigm,
    and produces all results necessary to plot a single figure.

    'props' is a vector containing proportions, one proportion per replication
    """

    if not configs.Eval.categorize_by_template:
        templates = ['all templates']
    else:
        raise NotImplementedError  # TODO read template info directly from local text files containing sentences

    group_names = list(group2predictions_file_paths.keys())
    group_names_with_controls = group_names + configs.Data.control_names

    # init result: a vector populated with accuracies, one for each model rep, per group, per template
    to_reps = lambda gn: configs.Eval.num_control_reps if 'baseline' in gn else len(group2predictions_file_paths[gn])
    res = {template: {gn: np.zeros(to_reps(gn)) for gn in group_names_with_controls}
           for template in templates}

    for group_name in group_names_with_controls:
        print(group_name)

        # generate control data
        if group_name in configs.Data.control_names:
            data_instances = [DataControl(group_name, phenomenon, paradigm)
                              for _ in range(configs.Eval.num_control_reps)]

        # read experimental data
        else:
            fps = group2predictions_file_paths[group_name]
            if not fps:
                print(f'Did not find prediction files. Consider reducing max step. Skipping')
                continue
            data_instances = [DataExperimental(fp, phenomenon, paradigm) for fp in fps]

        for row_id, data in enumerate(data_instances):

            # organize sentence pairs by template
            if configs.Eval.categorize_by_template:
                raise NotImplementedError
            else:
                template2pairs = {templates[0]: data.pairs}

            for template in templates:
                print(template)

                pairs = template2pairs[template]
                assert pairs

                # calc proportion correct - sentences on odd lines are bad, and sentences on even lines are good
                grammatical_scores: List[Tuple[bool, bool]] = [(False, True) for _ in pairs]
                num_correct = count_correct_choices(pairs, grammatical_scores, data.s2cross_entropies)
                prop = num_correct / len(pairs)

                # populate vector of proportions - one vector per model group
                res[template][group_name][row_id] = prop

    return res
