
"""
Something we really need to do next is to improve score_predictions() 
so that we can input multiple prediction files that represent the predictions of a whole group of BERT models. 
Currently we are only comparing predictions between single models, instead of groups of models. 
A group of models would be simply a group of prediction files which would be assigned the same bar color in the graph. 
You know what I'm saying? 
In the end, each bar should represent an average proportion (average of the proportions belonging to a group of models). 
That said, it would be useful to add error bars, indicating the standard deviation, for each bar in the graph. 
Take your time with this one.
"""
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

def score_multiple_models(sentence_file_names, categorize_templates_calculate_avg_std):

    for sentence_file_name in sentence_file_names:
        reader = Reader(sentence_file_name)
        test_sentence_list = reader.bert_predictions
        average_dict, std_dict = categorize_templates_calculate_avg_std(sentence_file_names, sentence_file_name, test_sentence_list)

    return average_dict, std_dict 






