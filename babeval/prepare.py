from typing import Dict, List, Callable, Tuple
import numpy as np
from pathlib import Path

from babeval.reader import Reader


def prepare_data_for_barplot(group2predictions_file_paths: Dict[str, List[Path]],
                             templates: List[str],
                             prediction_categories: Tuple,
                             categorize_by_template: Callable,
                             categorize_predictions: Callable,
                             print_stats: Callable) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param templates: list of names for templates, one for each subplot
    :param prediction_categories: categories for classifying productions made by model
    :param categorize_by_template: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :param print_stats: function to print basic information about sentences (optional)
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    Multiple frequency-control groups are added.

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a 2D array (matrix) containing proportions organized by category (in rows) and replications (in columns)
    """
    control_name_1gram = '1-gram-distribution control'
    control_name_left_2gram = 'left 2-gram-distribution control'
    control_name_right_2gram = 'right 2-gram-distribution control'

    group_names = list(group2predictions_file_paths.keys())
    control_group_names = [control_name_1gram, control_name_left_2gram, control_name_right_2gram]
    group_names_with_controls = group_names + control_group_names
    template2group_name2props = {template: {gn: None for gn in group_names_with_controls}
                                 for template in templates}

    for group_name in group_names_with_controls:
        print(f'===============\n{group_name}\n===============')

        if group_name in control_group_names:
            predictions_file_paths = group2predictions_file_paths[group_names[0]]
        else:
            predictions_file_paths = group2predictions_file_paths[group_name]

        for row_id, predictions_file_path in enumerate(predictions_file_paths):
            print(predictions_file_path)

            # read test sentences file with input and sentences in column1 and column 2 respectively
            reader = Reader(predictions_file_path)
            if group_name == control_name_1gram:
                sentences_out = reader.sentences_out_unigram_distribution_control
            elif group_name == control_name_left_2gram:
                sentences_out = reader.sentences_out_left_bigram_distribution_control
            elif group_name == control_name_right_2gram:
                sentences_out = reader.sentences_out_right_bigram_distribution_control
            else:
                sentences_out = reader.sentences_out

            print_stats(sentences_out)
            template2sentences_out, template2mask_index = categorize_by_template(reader.sentences_in,
                                                                                 sentences_out)

            for template in templates:
                print(template)

                # organize by sentence template
                category2num_in_category = categorize_predictions(template2sentences_out[template],
                                                                  template2mask_index[template])

                # calc proportion and store in matrix
                for col_id, category in enumerate(prediction_categories):
                    prop = category2num_in_category[category] / len(template2sentences_out[template])
                    # initialize matrix for storing proportions
                    if template2group_name2props[template][group_name] is None:
                        num_rows = len(predictions_file_paths)
                        num_cols = len(category2num_in_category)
                        template2group_name2props[template][group_name] = np.zeros((num_rows, num_cols))
                    # populate matrix
                    template2group_name2props[template][group_name][row_id][col_id] = prop

    return template2group_name2props


def prepare_data_for_scatterplot(group2predictions_file_paths: Dict[str, List[Path]],
                                 w2max_bigram_f: Dict[str, int],
                                 bigram2f: Dict[str, int],
                                 direction: str,
                                 replace_zeros_with_one: bool = True,
                                 ) -> Dict[str, Tuple[List[int], List[int]]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param w2max_bigram_f: dict mapping word to frequency of most frequent bigram in which word participates
    :param bigram2f: dict mapping bigram to frequency in corpus
    :param direction: "left" or "right"
    :param replace_zeros_with_one: when True, replace yi = 0 with yi = 1 to prevent log(yi) = -inf
    :return: x, y - the coordinates for a scatterplot
    """

    group_names = list(group2predictions_file_paths.keys())

    res = {g: ([], []) for g in group_names}

    for group_name in group_names:
        print(f'===============\n{group_name}\n===============')

        predictions_file_paths = group2predictions_file_paths[group_name]

        for row_id, predictions_file_path in enumerate(predictions_file_paths):
            print(predictions_file_path)

            # read test sentences file with input and sentences in column1 and column 2 respectively
            reader = Reader(predictions_file_path)

            for s1, s2 in zip(reader.sentences_in, reader.sentences_out):
                mask_index = s1.index('[MASK]')

                # xi
                if direction == 'left':
                    bigram = (s2[mask_index - 1], s2[mask_index])
                    xi = w2max_bigram_f[s2[mask_index - 1]]
                elif direction == 'right':
                    bigram = (s2[mask_index], s2[mask_index + 1])
                    xi = w2max_bigram_f[s2[mask_index + 1]]
                else:
                    raise AttributeError('Invalid arg to "direction"')

                # yi
                try:
                    yi = bigram2f[bigram]
                except KeyError:  # dict does not have word pieces
                    if replace_zeros_with_one:
                        yi = 1  # technically incorrect, but prevents log(0) = -inf
                    else:
                        yi = 0

                res[group_name][0].append(xi)
                res[group_name][1].append(yi)

    return res

