
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
import numpy as np
from babeval.reader import Reader

def score_multiple_models(divide_chunks, templates, categorize_templates, categorize_predictions, sentence_file_names):

    title2file_name2props = {template: {fn: [] for fn in sentence_file_names} for template in templates}

    for sentence_file_name in sentence_file_names:
        reader = Reader(sentence_file_name)
        test_sentence_list = reader.bert_predictions
        template2sentences = categorize_templates(test_sentence_list)

        for template in templates:
            predictions = categorize_predictions(template2sentences[template])

            for category, sentences_in_category in predictions.items():
                prop = len(sentences_in_category) / len(template2sentences[template])
                title2file_name2props[template][sentence_file_name].append(prop)

    """
    Add up all values of proportions of the second layer of the dict based on index
    Get averages and standard deviations and store values into two separate lists
    """

    lst = []
    for template in templates:
        for name in sentence_file_names:  
            lst.append(title2file_name2props[template][name])

    keys = ["average", "standard deviation"]

    average_dict = {keys[0]:{i: [] for i in range(len(title2file_name2props))}}
    std_dict = {keys[1]:{i: [] for i in range(len(title2file_name2props))}}

    n = len(sentence_file_names)
    #length of sentence_file_names = number of models

    value_lst = divide_chunks(lst,n) 

    for value, i in zip(value_lst, range(len(title2file_name2props))):
        value_array = np.array(value)
        avg = np.mean(value_array, axis=0)
        std = np.std(value_array, axis=0)
        average_dict[keys[0]][i].append(avg)
        std_dict[keys[1]][i].append(std)

    return average_dict, std_dict


