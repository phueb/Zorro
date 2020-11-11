
from zorro.agreement_across_RC.shared import task_name, plural, pronouns_3p, pronouns_1p_2p
from zorro.task_words import get_task_word_combo
from zorro.vocab import get_vocab_words

NUM_ADJECTIVES = 2
NUM_NOUNS = 2

template1a = 'the {} that {} like {} {} .'
template1b = 'the {} that {} likes {} {} .'
template2a = 'the {} that is there {} {} .'
template2b = 'the {} that are there {} {} .'

rules = {
    ('NN', 0, NUM_NOUNS): [  # todo make the tag a list to specify both singular + plural nouns in same slot
        template1a.format('{}', 'i', 'is', '_'),
        template2a.format('{}', 'is', '_'),
    ],

    ('JJ', 0, NUM_ADJECTIVES): [
        template1a.format('_', 'i', 'is', '{}'),
        template2a.format('_', 'is', '{}'),
    ],

}


def main():
    """
    example:
    "the dog that i like is green" vs. "the dogs that i like is green"
    """
    noun_plurals = get_vocab_words(tag='NNS')

    for noun_s, adj in get_task_word_combo(task_name, rules.keys()):
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals:
            continue

        # object-relative
        for pronoun_1p_2p in pronouns_1p_2p:
            yield template1a.format(noun_s, pronoun_1p_2p, 'is', adj)
            yield template1a.format(noun_s, pronoun_1p_2p, 'are', adj)
            yield template1a.format(noun_p, pronoun_1p_2p, 'is', adj)
            yield template1a.format(noun_p, pronoun_1p_2p, 'are', adj)
        for pronoun_3p in pronouns_3p:
            yield template1b.format(noun_s, pronoun_3p, 'is', adj)
            yield template1b.format(noun_s, pronoun_3p, 'are', adj)
            yield template1b.format(noun_p, pronoun_3p, 'is', adj)
            yield template1b.format(noun_p, pronoun_3p, 'are', adj)

        # subject-relative
        yield template2a.format(noun_s, 'is', adj)
        yield template2a.format(noun_s, 'are', adj)
        yield template2b.format(noun_p, 'is', adj)
        yield template2b.format(noun_p, 'are', adj)


if __name__ == '__main__':
    for s in main():
        print(s)
