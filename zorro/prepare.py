from typing import Dict, List, Callable, Tuple
import numpy as np
from pathlib import Path

from zorro.forced_choice import check_pairs_for_grammar, count_correct_choices
from zorro.data import DataExperimental, DataControl
from zorro import configs


def prepare_data_for_plotting(group2predictions_file_paths: Dict[str, List[Path]],
                              paradigm: str,
                              templates: List[str],
                              categorize_by_template: Callable,
                              grammar_checker: Callable,
                              ) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param paradigm: name of task, used to make control data
    :param templates: list of names for templates, one for each subplot
    :param categorize_by_template: function for separating sentences by template
    :param grammar_checker: function for checking grammar of each sentence in a pair
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    Multiple frequency-control groups are added.

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a vector containing proportions, one proportion per replication
    """

    group_names = list(group2predictions_file_paths.keys())
    group_names_with_controls = group_names + configs.Data.control_names

    # result - template2group_name2props
    res = {template: {gn: None for gn in group_names_with_controls}
           for template in templates}

    for group_name in group_names_with_controls:
        print(f'===============\n{group_name}\n===============')

        # read experimental, or generate control data
        if group_name in configs.Data.control_names:
            data_instances = [DataControl(group_name, paradigm) for _ in range(configs.Eval.num_control_reps)]
        else:
            data_instances = [DataExperimental(fp, paradigm) for fp in group2predictions_file_paths[group_name]]

        for row_id, data in enumerate(data_instances):

            # organize sentence pairs by template
            template2pairs = categorize_by_template(data.pairs)

            for template in templates:
                print(template)
                print()

                pairs = template2pairs[template]
                assert pairs

                # calc proportion correct
                grammatical_scores = check_pairs_for_grammar(pairs, grammar_checker)
                num_correct = count_correct_choices(pairs, grammatical_scores, data.s2cross_entropies)
                prop = num_correct / len(pairs)

                # init vector of proportions - one proportion for each replication of a model
                if res[template][group_name] is None:
                    num_rows = len(data_instances)
                    res[template][group_name] = np.zeros(num_rows)

                # populate vector of proportions - one vector per model group
                res[template][group_name][row_id] = prop

    return res
