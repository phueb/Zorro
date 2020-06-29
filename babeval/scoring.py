from typing import Dict, List, Callable
import numpy as np

from babeval.reader import Reader


def score_predictions(group2predictions_file_paths: Dict[str, List[str]],
                      templates: List[str],
                      categorize_by_template: Callable,
                      categorize_predictions: Callable,
                      print_stats: Callable) -> Dict[str, Dict[str, np.array]]:
    """
    :param group2predictions_file_paths: dict mapping group name to paths of files containing predictions
    :param templates: list of names for templates, one for each subplot
    :param categorize_by_template: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :param print_stats: function to print basic information about sentences (optional)
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    A frequency-control group is added

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a 2D array (matrix) containing proportions organized by category (in rows) and replications (in columns)
    """
    control_name = 'frequency-based control'
    group_names = list(group2predictions_file_paths.keys())
    group_names_with_controls = group_names + [control_name]
    template2group_name2props = {template: {gn: None for gn in group_names_with_controls}
                                 for template in templates}

    for group_name in group_names_with_controls:
        print(f'===============\nScoring {group_name}\n===============')

        if group_name == control_name:
            predictions_file_paths = group2predictions_file_paths[group_names[0]]
        else:
            predictions_file_paths = group2predictions_file_paths[group_name]

        for template in templates:
            print(template)

            for row_id, predictions_file_path in enumerate(predictions_file_paths):
                print(predictions_file_path)

                # read test sentences file with input and output in column1 and column 2 respectively
                if group_name == control_name:
                    reader = Reader(predictions_file_path)
                    print_stats(reader.sentences_out_random_control)
                    template2sentences = categorize_by_template(reader.sentences_in,
                                                                reader.sentences_out_random_control)
                else:
                    reader = Reader(predictions_file_path)
                    print_stats(reader.sentences_out)
                    template2sentences = categorize_by_template(reader.sentences_in,
                                                                reader.sentences_out)

                # organize by sentence template
                category2sentences = categorize_predictions(template2sentences[template])

                # calc proportion and store in matrix
                for col_id, (category, sentences) in enumerate(category2sentences.items()):
                    prop = len(sentences) / len(template2sentences[template])
                    # initialize matrix for storing proportions
                    if template2group_name2props[template][group_name] is None:
                        num_rows = len(predictions_file_paths)
                        num_cols = len(category2sentences)
                        template2group_name2props[template][group_name] = np.zeros((num_rows, num_cols))
                    # populate matrix
                    template2group_name2props[template][group_name][row_id][col_id] = prop

            print(template2group_name2props[template][group_name].round(2))
            print()

    return template2group_name2props
