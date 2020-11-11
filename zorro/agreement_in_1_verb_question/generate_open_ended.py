from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words
from zorro.agreement_in_1_verb_question.shared import task_name, plural
from zorro import configs

NUM_NOUNS = 4

template1 = 'where' + f' {configs.Data.mask_symbol} ' + 'the {} ?'
template2 = 'what' + f' {configs.Data.mask_symbol} ' + 'the {} ?'


def main():
    """

    """
    noun_plurals = get_vocab_words(tag='NNS')

    for (noun_s,) in get_task_word_combo(task_name, (('NN', 0, NUM_NOUNS),
                                                     )):
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals:
            continue

        yield template1.format(noun_s)
        yield template2.format(noun_p)


if __name__ == '__main__':
    for s in main():
        print(s)