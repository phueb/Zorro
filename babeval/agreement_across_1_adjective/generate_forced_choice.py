
from babeval import configs
from babeval.task_words import get_task_word_combo
from babeval.whole_words import get_whole_words

NUM_ADJECTIVES = 2
NUM_NOUNS  = 2

template1 = 'look at {} {} {} .'
template2 = '{} {} {} went there .'

rules = {
    ('JJ', 0, NUM_ADJECTIVES): [
        template1.format('this', '{}', '_'),
        template2.format('this', '{}', '_'),
    ],
    ('NN', 0, NUM_NOUNS): [
        template1.format('this', '_', '{}'),
        template2.format('this', '_', '{}'),
    ],
}


def main():
    """
    example:
    "look at this green house ." vs. "look at this green houses ."
    "this green house went there ." vs. "this green houses went there."
    """
    from babeval.agreement_across_1_adjective.common import task_name, pre_nominals

    for pre_nominal in pre_nominals:
        for words in get_task_word_combo(task_name, rules.keys()):

            noun_plural = f'{words[1]}s'  # TODO also handle irregular plurals
            if noun_plural not in get_whole_words(tag='NNS'):
                continue
            words2 = [words[0], noun_plural]

            yield template1.format(pre_nominal, *words)
            yield template1.format(pre_nominal, *words2)

            yield template2.format(pre_nominal, *words)
            yield template2.format(pre_nominal, *words2)


for i in main():
    print(i)