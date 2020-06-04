
class Reader:
    def __init__(self, predictions_file_name):

        self.test_sentence_list = self.reformat_BERT_output(predictions_file_name)

    def reformat_BERT_output(self, sentence_file_name):
        file = open(sentence_file_name, "r")
        lines = file.readlines()
        file.close()

        col2 = []
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                col2.append(parts[-1])

        test_sentence_list = [[]]
        for w in col2:
            test_sentence_list[-1].append(w)
            if w == '.':
                test_sentence_list.append([])

        if not test_sentence_list[-1]:
            del test_sentence_list[-1]

        return test_sentence_list