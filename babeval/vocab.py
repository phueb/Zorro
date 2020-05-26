from pathlib import Path


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