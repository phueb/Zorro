import nltk
from pathlib import Path
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

wnl = WordNetLemmatizer()


def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    return True if word is not lemma else False


def get_vocab(name, num_words=4096):
    path = Path(name)
    with open(path) as f:
        text_string_list = []
        text_string = f.read().split()
        text_string_list.append(text_string)
        my_list = [t[1::2] for t in text_string_list]
        for lst in my_list:
            result = lst[:num_words]
    return result


def classify_vocab(vocab):

    result = dict()

    pos_list = nltk.pos_tag(vocab)
    result['nouns'] = sorted([token[0] for token in pos_list if token[1] in ['NN', 'NNS', 'NNP', 'NNPS']])
    result['verbs'] = sorted([token[0] for token in pos_list if token[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']])
    result['adjectives'] = sorted([token[0] for token in pos_list if token[1] in ['JJ', 'JJR', 'JJS']])

    # separate plural from singular nouns
    result['nouns_singular'] = [noun for noun in result['nouns'] if not isplural(noun)]
    result['nouns_plural'] = [noun for noun in result['nouns'] if isplural(noun)]

    return result
