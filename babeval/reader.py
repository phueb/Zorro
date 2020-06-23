import numpy as np
from pathlib import Path

from babeval.vocab import get_vocab, get_frequency


class Reader:
    def __init__(self, predictions_file_name):

        self.predictions_file_name = predictions_file_name
        self.col1, self.col2 = self.get_columns()

        self.bert_predictions = self.get_bert_predictions()
        self.rand_predictions = self.get_random_predictions()

    def get_columns(self):
        path = Path(__file__).parent.parent / 'prediction_files' / self.predictions_file_name
        lines = path.open().readlines()

        col1 = [[]]
        col2 = [[]]
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                col1[-1].append(parts[0])
                col2[-1].append(parts[1])
            else:
                col1.append([])
                col2.append([])

        if not col1[-1]:
            del col1[-1]
        if not col2[-1]:
            del col2[-1]

        return col1, col2

    def get_bert_predictions(self):

        result = self.col2
        return result

    def get_random_predictions(self):
        vocab = get_vocab()
        freq = get_frequency()
        freq[vocab.index('.')] = 0  # tell random sampler to never sample a period
        weights = np.array(freq) / sum(freq)

        result = []
        for s in self.col1:
            for n, w in enumerate(s):
                if w == '[MASK]':
                    s[n] = np.random.choice(vocab, p=weights)
            result.append(s)

        return result
