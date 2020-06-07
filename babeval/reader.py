import numpy as np
import sys, os

from babeval.vocab import get_vocab, get_frequency

class Reader:
    def __init__(self, predictions_file_name):

        self.predictions_file_name = predictions_file_name
        self.col1, self.col2 = self.get_columns()

        self.bert_predictions = self.get_bert_predictions()
        self.rand_predictions = self.get_random_predictions()

    def get_columns(self):
        file = open(self.predictions_file_name, "r")
        lines = file.readlines()
        file.close()

        col1 = []
        col2 = []
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                col1.append(parts[0])
                col2.append(parts[1])

        return col1, col2

    def get_bert_predictions(self):

        result = [[]]
        for w in self.col2:
            result[-1].append(w)
            if w == '.':
                result.append([])

        if not result[-1]:
            del result[-1]

        return result


    def get_random_predictions(self):
        vocab = get_vocab()
        freq = get_frequency()
        lst = list(zip(vocab, freq))
        clean_freq_lst = [ele2 for ele1, ele2 in lst if ele1 != "."]
        freq_sum = sum(clean_freq_lst)

        weights_lst = []
        for f in clean_freq_lst:
            weights = f/freq_sum
            weights_lst.append(weights)

        result = [[]]
        for w in self.col1:

            if w == '[MASK]':
                w = np.random.choice([i for i in vocab if i != "."], p = weights_lst)
            result[-1].append(w)
            #ValueError: a must be 1-dimensional or an integer

            if w == '.':
                result.append([])

        if not result[-1]:
            del result[-1]

        return result
