from numpy.random import default_rng 
rng = default_rng()

import sys, os
sys.path.append(os.path.abspath(os.path.join('..'))) 
from vocab import get_vocab
from reader import Reader

class Random_Predictions:
    def __init__(self, test_sentence_list):

        self.random_predictions_list = self.get_random_predictions(test_sentence_list)

    def get_random_predictions(self, test_sentence_list):
        
        word_list = get_vocab()

        random_numbers = rng.choice(len(word_list), size=len(test_sentence_list), replace=True)
        
        random_predictions_list = []
        
        for sentence, i in zip(test_sentence_list, random_numbers):
            sentence[-2] = word_list[i]
            random_predictions_list.append(sentence)
        
        return random_predictions_list
