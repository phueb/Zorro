import spacy
import json
from pathlib import Path

from babeval import configs



def get_whole_words():
    path = Path(__file__).parent.parent / VOCAB_NAME
    with open(path) as f:
        text_string_list = []
        text_string = f.read().split()
        text_string_list.append(text_string)
        my_list = [t[1::2] for t in text_string_list][0]

    return my_list[:VOCAB_SIZE]


def get_frequency():
    path = Path(__file__).parent.parent / VOCAB_NAME
    with open(path) as f:
        text_string_list = []
        text_string = f.read().split()
        text_string_list.append(text_string)
        freq = [t[::2] for t in text_string_list][0]
        my_freq = [int(i) for i in freq if i.isdigit()]

    return my_freq[:VOCAB_SIZE]

