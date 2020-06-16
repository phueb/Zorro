"""
Something we really need to do next is to improve score_predictions() 
so that we can input multiple prediction files that represent the predictions of a whole group of BERT models. 
Currently we are only comparing predictions between single models, instead of groups of models. 
A group of models would be simply a group of prediction files which would be assigned the same bar color in the graph. 
You know what I'm saying? 
In the end, each bar should represent an average proportion (average of the proportions belonging to a group of models)
That said, it would be useful to add error bars, indicating the standard deviation, for each bar in the graph. 
Take your time with this one.
"""
from pathlib import Path
from os import walk
import numpy as np

from babeval.visualizer import Visualizer
from babeval.scoring_multiple import score_multiple_models

#ONE PREDICTIN FILE = ONE ADDITIONAL MODEL
#AVERAGE PROPORTION SHOULD BE DISPLAYED AS SINGLE BAR

#read file names from the predictions_file folder
prediction_file_names = []
my_path = Path().cwd()/"(dummy)prediction_files"
for (dirpath, dirnames, filenames) in walk(my_path):
    prediction_file_names.extend(filenames)
    if '.DS_Store' in prediction_file_names: # '.DS_Store' automatically added by MAC system
        prediction_file_names.remove('.DS_Store')
    break

#key words to locate different templates 
key_word = ["look", "?"] 

def categorize_templates_calculate_avg_std(sentence_file_names, sentence_file_name, test_sentence_list):
    """
    Categorize files into different templates
    Call functions from corresponding script if the file belongs to the template
    """
    for sentence in test_sentence_list:
        #TODO: try think of a better way to categorize

        if sentence[0] == key_word[0]: #adj
            from agreement_across_adjectives import score
            from agreement_across_adjectives.score import templates

        if sentence[-1] == key_word[1]: #question
            from agreement_in_question import score
            from agreement_in_question.score import templates

    template2sentences = score.categorize_templates(test_sentence_list)
    title2file_name2props = {template: {fn: [] for fn in sentence_file_names} for template in templates}

    for template in templates:
            predictions = score.categorize_predictions(template2sentences[template])

            for category, sentences_in_category in predictions.items():
                prop = len(sentences_in_category) / len(template2sentences[template])
                title2file_name2props[template][sentence_file_name].append(prop)

    """
    Add up all values of proportions of the second layer of the dict based on index
    Get averages and standard deviations and store values into two separate lists
    """
    lst = []
    for template in templates:
        for name in prediction_file_names:  
            lst.append(title2file_name2props[template][name])

    keys = ["average", "standard deviation"]

    average_dict = {keys[0]:{i: [] for i in range(len(title2file_name2props))}}
    std_dict = {keys[1]:{i: [] for i in range(len(title2file_name2props))}}

    for i in range(len(title2file_name2props)):
        value_lst = [lst[i], lst[i + len(title2file_name2props)]]
        value_array = [np.array(x) for x in value_lst]
        avg = [np.mean(k) for k in zip(*value_array)] 
        std = [np.std(k) for k in zip(*value_array)]

        average_dict[keys[0]][i].append(avg)
        std_dict[keys[1]][i].append(std)

    return average_dict, std_dict

# score
average_dict, std_dict = score_multiple_models(prediction_file_names, categorize_templates_calculate_avg_std)

x_tick_labels = ("[UNK]", "correct\nnoun", "false\nnoun", "ambiguous\nnoun", "non-noun")

# plot
visualizer = Visualizer()
visualizer.make_barplot_for_multiple_models(x_tick_labels, average_dict, std_dict)