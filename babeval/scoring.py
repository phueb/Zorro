from babeval.reader import Reader


def score_predictions(sentence_file_names, templates, categorize_templates, categorize_predictions, print_stats):
    """

    :param sentence_file_names: list of file names containing predictions
    :param templates: list of names for templates, one for each subplot
    :param categorize_templates: function for separating sentences by template
    :param categorize_predictions: function for scoring
    :param print_stats: function to print basic information about sentences (optional)
    :return: double-embedded dict, which can be input to barplot function

    how it works: for each prediction file:
    1. a frequency-control is added
    2. the predictions are read and categorized by template and production category (eg. false, correct, etc)
    3. information is stored in double-embedded dict, which can be input to barplot function
    """
    control_name = '_frequency-based control'
    sentence_file_names = list(sentence_file_names) + \
                          [name + control_name for name in sentence_file_names]
    title2file_name2props = {template: {fn: [] for fn in sentence_file_names} for template in templates}

    for sentence_file_name in sentence_file_names:
        print(f'Scoring {sentence_file_name}')

        if sentence_file_name.endswith(control_name):
            reader = Reader(sentence_file_name.replace(control_name, ''))
            print_stats(reader.rand_predictions)
            template2sentences = categorize_templates(reader.rand_predictions)
        else:
            reader = Reader(sentence_file_name)
            print_stats(reader.bert_predictions)
            template2sentences = categorize_templates(reader.bert_predictions)

        for template in templates:
            predictions = categorize_predictions(template2sentences[template])

            for category, sentences_in_category in predictions.items():
                prop = len(sentences_in_category) / len(template2sentences[template])
                title2file_name2props[template][sentence_file_name].append(prop)

    return title2file_name2props
