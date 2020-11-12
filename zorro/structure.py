from typing import Dict, List, Callable, Tuple
import numpy as np
from pathlib import Path

from zorro.data import DataExpOpenEnded, DataCtlOpenEnded
from zorro.data import DataExpForcedChoice, DataCtlForcedChoice
from zorro import configs


def prepare_data_for_barplot_open_ended(group2predictions_file_paths: Dict[str, List[Path]],
                                        templates: List[str],
                                        prediction_categories: Tuple,
                                        categorize_by_template: Callable,
                                        categorize_predictions: Callable,
                                        ) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param templates: list of names for templates, one for each subplot
    :param prediction_categories: categories for classifying productions made by model
    :param categorize_by_template: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    Multiple frequency-control groups are added.

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a 2D array (matrix) containing proportions organized by category (in rows) and replications (in columns)
    """
    group_names = list(group2predictions_file_paths.keys())
    group_names_with_controls = group_names + configs.Data.control_names

    # get a path to experimental data file so that control data can be generated based on experimental data format
    control_fp = group2predictions_file_paths[group_names[0]][0]

    res = {template: {gn: None for gn in group_names_with_controls}
           for template in templates}

    for group_name in group_names_with_controls:
        print(f'===============\n{group_name}\n===============')

        # read experimental, or generate control data
        if group_name in configs.Data.control_names:
            data_instances = [DataCtlOpenEnded(control_fp, group_name) for _ in range(configs.Eval.num_control_reps)]
        else:
            data_instances = [DataExpOpenEnded(fp) for fp in group2predictions_file_paths[group_name]]

        for row_id, data in enumerate(data_instances):

            template2sentences_out, template2mask_index = categorize_by_template(data.sentences_in,
                                                                                 data.sentences_out)

            for template in templates:
                assert template2sentences_out[template]
                assert template2mask_index[template]

                # organize by sentence template
                category2num_in_category = categorize_predictions(template2sentences_out[template],
                                                                  template2mask_index[template])

                # calc proportion and store in matrix
                for col_id, category in enumerate(prediction_categories):
                    prop = category2num_in_category[category] / len(template2sentences_out[template])
                    # initialize matrix for storing proportions
                    if res[template][group_name] is None:
                        num_rows = len(data_instances)
                        num_cols = len(category2num_in_category)
                        res[template][group_name] = np.zeros((num_rows, num_cols))
                    # populate matrix
                    res[template][group_name][row_id][col_id] = prop

    return res


def prepare_data_for_barplot_forced_choice(group2predictions_file_paths: Dict[str, List[Path]],
                                           task_name: str,
                                           templates: List[str],
                                           prediction_categories: Tuple,
                                           categorize_by_template: Callable,
                                           categorize_predictions: Callable,
                                           ) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param task_name: name of task, used to make control data
    :param templates: list of names for templates, one for each subplot
    :param prediction_categories: categories for classifying productions made by model
    :param categorize_by_template: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    Multiple frequency-control groups are added.

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a 2D array (matrix) containing proportions organized by category (in rows) and replications (in columns)
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
            data_instances = [DataCtlForcedChoice(group_name, task_name) for _ in range(configs.Eval.num_control_reps)]
        else:
            data_instances = [DataExpForcedChoice(fp, task_name) for fp in group2predictions_file_paths[group_name]]

        for row_id, data in enumerate(data_instances):

            # organize sentence pairs by template
            template2s2s = categorize_by_template(data.pairs)

            for template in templates:
                print(template)
                print()

                assert template2s2s[template]

                # categorize sentence pairs in template as "correct" or "false"
                category2num_in_category = categorize_predictions(template2s2s[template],
                                                                  data.s2cross_entropies)

                # calc proportion and store in matrix
                for col_id, category in enumerate(prediction_categories):
                    prop = category2num_in_category[category] / len(template2s2s[template])
                    # initialize matrix for storing proportions
                    if res[template][group_name] is None:
                        num_rows = len(data_instances)
                        num_cols = len(category2num_in_category)
                        res[template][group_name] = np.zeros((num_rows, num_cols))
                    # populate matrix
                    res[template][group_name][row_id][col_id] = prop

    return res
