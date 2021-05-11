import random

NUM_NOUNS = 90

template1 = 'where {} the {} go ?'
template2 = 'what {} the {} do ?'

rules = {
    ('NN', 0, NUM_NOUNS): [
        template1.format('does', '{}'),
        template2.format('does', '{}'),
    ],
}


def main():
    """
    example:
    "where does the dog go?"
    "what does the dog do?"
    """

    from zorro.agreement_in_2_verb_question.shared import paradigm, plural
    from zorro.agreement_in_2_verb_question.shared import doing_plural, doing_singular
    from zorro.task_words import get_task_words
    from zorro.vocab import get_vocab_words
    from zorro import configs

    noun_plurals = get_vocab_words(tag='NNS')
    nouns_s = get_task_words(paradigm, tag='NN', num_words_in_sample=NUM_NOUNS)

    num_pairs = 0

    while num_pairs < configs.Data.num_pairs_per_paradigm:

        # TODO this paradigm creates duplicates

        noun_s = random.choice(nouns_s)
        noun_p = plural.plural(noun_s)
        if noun_p not in noun_plurals or noun_p == noun_s:
            continue

        # random choices
        doing = random.choice(doing_singular + doing_plural)

        yield template1.format(doing, noun_s)
        yield template1.format(doing, noun_p)

        yield template2.format(doing, noun_s)
        yield template2.format(doing, noun_p)

        num_pairs += 2


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2:>12,}', s)
