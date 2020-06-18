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
from babeval.reader import Reader

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
key_word = ["look", "?", "the", "that"] 

#TODO: try think of a better way to call corresponding script

#call different scripts based on structures of test sentences

for sentence_file_name in prediction_file_names:
    reader = Reader(sentence_file_name)
    test_sentence_list = reader.bert_predictions

    for sentence in test_sentence_list:
        if sentence[0] == key_word[0]: #adj
            from agreement_across_adjectives.score import categorize_templates, categorize_predictions
            from agreement_across_adjectives.score import templates

        elif sentence[-1] == key_word[1]: #question
            from agreement_in_question.score import categorize_templates, categorize_predictions
            from agreement_in_question.score import templates

        elif sentence[0] == key_word[2] and sentence[3] == key_word[2]: #PP
            from agreement_across_PP.score import categorize_templates, categorize_predictions
            from agreement_across_PP.score import templates

        elif sentence[0] == key_word[2] and sentence[2] == key_word[3]: #RC
            from agreement_across_RC.score import categorize_templates, categorize_predictions
            from agreement_across_RC.score import templates

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

# score
average_dict, std_dict = score_multiple_models(divide_chunks, templates, categorize_templates, categorize_predictions, prediction_file_names)

x_tick_labels = ("[UNK]", "correct\nnoun", "false\nnoun", "ambiguous\nnoun", "non-noun")

# plot
# visualizer = Visualizer()
# visualizer.make_barplot_for_multiple_models(x_tick_labels, average_dict, std_dict)