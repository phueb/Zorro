
from zorro import configs
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words
from zorro.agreement_across_PP.shared import task_name, plural


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
    1. use equal proportion of sentences containing plural vs. singular object nouns
    """

    noun_plurals = get_vocab_words(tag='NNS')

    for sub_s, obj_s, adj in get_task_word_combo(task_name,
                                                 [('NN', 0, NUM_NOUNS),
                                                  ('NN', 1, NUM_NOUNS),
                                                  ('JJ', 0, NUM_ADJECTIVES)
                                                  ]):

        sub_p = plural.plural(sub_s)
        obj_p = plural.plural(obj_s)
        if sub_p not in noun_plurals or obj_p not in noun_plurals:
            continue
        if sub_s == sub_p or obj_s == obj_p:  # exclude nouns with ambiguous number
            continue

        yield template1.format(sub_s, obj_s, adj)
        yield template1.format(sub_s, obj_p, adj)
        yield template1.format(sub_p, obj_s, adj)
        yield template1.format(sub_p, obj_p, adj)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
