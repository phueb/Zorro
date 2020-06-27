import numpy as np

from babeval.vocab import get_vocab, get_frequency


class Reader:
    def __init__(self, predictions_file_path):

        self.predictions_file_path = predictions_file_path
        self.sentences_in, self.sentences_out = self.get_columns()
        self.sentences_out_random_control = self.get_sentences_out_random_control()

        print(f'Found {len(self.sentences_out)} lines in file.')

    def get_columns(self):
        lines = self.predictions_file_path.open().readlines()

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

    def get_sentences_out_random_control(self, not_sampled=None):
        """
        :param not_sampled: st, a word that should not be sampled from vocabulary
        :return: list of test sentences with MASK symbol replaced with random word from vocab
         sampled based on frequency in corpus
        """
        vocab = get_vocab()
        freq = get_frequency()
        if not_sampled is not None:
            freq[vocab.index(not_sampled)] = 0  # tell random sampler to never sample something
        weights = np.array(freq) / sum(freq)

        result = []
        for s in self.sentences_in:
            assert '[MASK]' in s, s
            s_new = [np.random.choice(vocab, p=weights) if w == '[MASK]' else w for w in s]
            result.append(s_new)

        return result
