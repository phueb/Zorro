import numpy as np
from babeval.vocab import get_vocab


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

        vocab, freq = get_vocab()
        freq.remove(freq[vocab.index('.')])
        vocab.remove('.')

        weights_lst = []
        freq_sum = sum([int(i) for i in freq if type(i)== int or i.isdigit()]) 
        for f in freq:
            weights = int(f)/freq_sum
            weights_lst.append(weights)

        # cum_weights = [0] + list(np.cumsum(weights_lst)).

        result = [[]]
        for w in self.col1:

            if w == '[MASK]':
                w = np.random.choice(vocab, p = weights_lst)  # FIXED
            result[-1].append(w)

            if w == '.':
                result.append([])

        if not result[-1]:
            del result[-1]

        return result
