import numpy as np

from babeval.reader import Reader


def score_predictions(group2sentence_file_names, templates, categorize_templates, categorize_predictions, print_stats):
    """
    :param group2sentence_file_names: dict mapping group name to file names containing predictions
    :param templates: list of names for templates, one for each subplot
    :param categorize_templates: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :param print_stats: function to print basic information about sentences (optional)
    :return: double-embedded dict, which can be input to barplot function
    how it works: for each group of prediction files:
    1. a frequency-control is added
    2. the prediction files are read and categorized by template and production category (eg. false, correct, etc)
    3. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    this functions scores all prediction files associated with a single task,
    and produces all results necessary to plot a single figure.

    'props' is a 2D array (matrix) containing proportions organized by category (in rows) and replications (in columns)
    """
    control_name = '_frequency-based control'
    group_names_with_controls = list(group2sentence_file_names.keys()) + \
                                [name + control_name for name in group2sentence_file_names.keys()]
    template2group_name2props = {template: {gn: None for gn in group_names_with_controls}
                                 for template in templates}

    for group_name in group_names_with_controls:
        print(f'===============\nScoring {group_name}\n===============')
        sentence_file_names = group2sentence_file_names[group_name.replace(control_name, '')]

        for template in templates:
            print(template)

            for row_id, sentence_file_name in enumerate(sentence_file_names):
                print(sentence_file_name)

                if group_name.endswith(control_name):
                    reader = Reader(sentence_file_name.replace(control_name, ''))
                    print_stats(reader.rand_predictions)
                    template2sentences = categorize_templates(reader.rand_predictions)
                else:
                    reader = Reader(sentence_file_name)
                    print_stats(reader.bert_predictions)
                    template2sentences = categorize_templates(reader.bert_predictions)

                category2sentences = categorize_predictions(template2sentences[template])

                # calc proportion and store in matrix
                for col_id, (category, sentences) in enumerate(category2sentences.items()):
                    prop = len(sentences) / len(template2sentences[template])
                    # initialize matrix for storing proportions
                    if template2group_name2props[template][group_name] is None:
                        print('initializing with zeros')
                        num_rows = len(sentence_file_names)
                        num_cols = len(category2sentences)
                        template2group_name2props[template][group_name] = np.zeros((num_rows, num_cols))
                    # populate matrix
                    template2group_name2props[template][group_name][row_id][col_id] = prop

            print(template2group_name2props[template][group_name].round(2))
            print()

    return template2group_name2props
