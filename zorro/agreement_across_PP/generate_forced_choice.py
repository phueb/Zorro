
from zorro.task_words import get_task_word_combo
from zorro.agreement_across_PP.shared import task_name


NUM_NOUNS = 2
NUM_ADJECTIVES = 2

template1 = 'the {} on the {} {} {} .'
template2 = 'the {} by the {} {} {} .'

rules = {
    ('NN', 0, NUM_NOUNS): [  # todo make the tag a list to specify both singular + plural nouns in same slot
        template1.format('{}', '_', 'is', '_'),
        template2.format('{}', '_', 'is', '_'),
    ],
    ('NNS', 0, NUM_NOUNS): [
        template1.format('{}', '_', 'are', '_'),
        template2.format('{}', '_', 'are', '_'),
    ],
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('_', '_', 'is/are', '{}'),
        template2.format('_', '_', 'is/are', '{}'),
    ],

}


def main():
    """
    example:
    "the dog on the mats is brown" vs "the dog on the mats are brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use opposite numbered object noun vs. subject noun  # todo it would be better to have 50/50 singular/plural object nouns
    """

    for words in get_task_word_combo(task_name, rules.keys()):

        # counter-balance singular vs plural with subj vs. obj
        for subject_id, object_id in [[0, 1], [1, 0]]:

            yield template1.format(words[subject_id], words[object_id], 'is' , words[2])
            yield template1.format(words[subject_id], words[object_id], 'are', words[2])


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
