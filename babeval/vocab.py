import nltk
from pathlib import Path
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')

wnl = WordNetLemmatizer()

excluded_words = open("excluded_words.txt", "r").read().split()

VOCAB_NAME = "childes-20191206_vocab.txt"  # fixed
VOCAB_SIZE = 4000  # fixed


def get_vocab():
    path = Path(__file__).parent.parent / VOCAB_NAME
    with open(path) as f:
        text_string_list = []
        text_string = f.read().split()
        text_string_list.append(text_string)
        my_list = [t[1::2] for t in text_string_list][0]
    return my_list[:VOCAB_SIZE]


def classify_vocab(vocab):

    result = dict()
    num_excluded = 0

    # each word must be tagged separately, otherwise nltk uses context to assign tag
    for w in sorted(vocab):
        tag = nltk.pos_tag([w])[0][1]

        if w in excluded_words:
            num_excluded += 1
            continue

        if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
            result.setdefault('nouns', []).append(w)
        if tag in ['NN', 'NNP'] or w.istitle():
            result.setdefault('nouns_singular', []).append(w)
        if tag in ['NNS', 'NNPS']:
            result.setdefault('nouns_plural', []).append(w)
        if tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            result.setdefault('verbs', []).append(w)
        if tag in ['JJ', 'JJR', 'JJS']:
            result.setdefault('adjectives', []).append(w)

    print(f'nouns     ={len(result["nouns"]):>9,}')
    print(f'nouns_sing={len(result["nouns_singular"]):>9,}')
    print(f'nouns_plur={len(result["nouns_plural"]):>9,}')
    print(f'verbs     ={len(result["verbs"]):>9,}')
    print(f'adjectives={len(result["adjectives"]):>9,}')

    print(f'excluded  ={num_excluded:>9,}')

    return result


def save_to_txt(words, file_name):
    output_folder = Path(__file__).parent.parent / "word_lists"
    out_path = output_folder / file_name
    with open(out_path, 'w') as f:
        for n, w in enumerate(words):
            f.write(w + '\n')


# TODO need native speaker

# TODO document dictonairy-based decisions

