
from zorro.agreement_across_RC.shared import task_name, plural, pronouns_3p, pronouns_1p_2p
from zorro import configs
from zorro.task_words import get_task_word_combo
from zorro.whole_words import get_whole_words

NUM_NOUNS = 4
NUM_ADJECTIVES = 4

# object-relative clause
template1a = 'the {} that {} like' + f' {configs.Data.mask_symbol} ' + '{} .'
template1b = 'the {} that {} likes' + f' {configs.Data.mask_symbol} ' + '{} .'
# subject-relative clause - contains hint about number in relative clause
template2a = 'the {} that is there' + f' {configs.Data.mask_symbol} ' + '{} .'
template2b = 'the {} that are there' + f' {configs.Data.mask_symbol} ' + '{} .'


def main():
    """
    example:
    "the dog that I like [MASK] lazy"
    """

    noun_plurals = get_whole_words(tag='NNS')

    for noun_s, adj in get_task_word_combo(task_name, (('NN', 0, NUM_NOUNS),
                                                       ('JJ', 0, NUM_ADJECTIVES),
                                                       )):
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals:
            continue

        # object-relative
        for pronoun_1p_2p in pronouns_1p_2p:
            yield template1a.format(noun_s, pronoun_1p_2p, adj)
            yield template1a.format(noun_p, pronoun_1p_2p, adj)
        for pronoun_3p in pronouns_3p:
            yield template1b.format(noun_s, pronoun_3p, adj)
            yield template1b.format(noun_p, pronoun_3p, adj)

        # subject-relative
        yield template2a.format(noun_s, adj)
        yield template2a.format(noun_s, adj)
        yield template2b.format(noun_p, adj)
        yield template2b.format(noun_p, adj)


if __name__ == '__main__':
    for s in main():
        print(s)
