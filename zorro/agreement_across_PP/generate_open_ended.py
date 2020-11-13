
from zorro import configs
from zorro.task_words import get_task_word_combo
from zorro.agreement_across_PP.shared import task_name


NUM_NOUNS = 2
NUM_ADJECTIVES = 4

template1 = 'the {} on the {}' + f' {configs.Data.mask_symbol} ' + '{} .'
template2 = 'the {} by the {}' + f' {configs.Data.mask_symbol} ' + '{} .'


def main():
    """
    example:
    "the dog on the mat <mask> brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of plural vs. singular object nouns n singular vs. plural sentences
    """

    for words in get_task_word_combo(task_name, (('NN', 0, NUM_NOUNS),
                                                 ('NNS', 0, NUM_NOUNS),
                                                 ('JJ', 0, NUM_ADJECTIVES)
                                                 )):

        # counter-balance singular vs plural with subj vs. obj
        for subject_id, object_id in [[0, 1], [1, 0]]:
            yield template1.format(words[subject_id], words[object_id], words[2])
            yield template1.format(words[subject_id], words[object_id], words[2])


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
