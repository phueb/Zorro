import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 100


def main():
    """
    example:
    "a big dog fell just now ." vs. "a big dog fallen just now ."

    """

    from zorro.irregular_past_participle_verb_intransitive.shared import paradigm, verbs_base, determiners
    from zorro.irregular_past_participle_verb_intransitive.shared import vb2vbd_vbn_intransitive as vb2vbd_vbn
    from zorro.task_words import get_task_words
    from zorro.vocab import get_vocab_words

    vocab = get_vocab_words()
    adjectives = get_task_words(paradigm, 'JJ', 0, NUM_ADJECTIVES)

    modifiers = ['just now', 'over there', 'some time ago', 'without us']

    for noun in get_task_words(paradigm, 'NN', 0, NUM_NOUNS):

        for verb_base in verbs_base:  # these are not counterbalanced across corpora (and probably need not)

            # template is specific to verb-class
            template = '{} {} {} {} {} .'.format(
                    random.choice(determiners),
                    random.choice(adjectives),
                    '{}',
                    '{}',
                    random.choice(modifiers))

            # get two contrasting irregular inflected forms
            try:
                vbd, vbn = vb2vbd_vbn[verb_base]  # past, past participle
            except KeyError:  # verb is not in irregular collection
                continue
            if (vbd not in vocab or vbn not in vocab) or vbd == vbn:
                print(f'"{verb_base:<22} excluded due to some forms not in vocab')
                continue

            # vbd is correct
            yield template.format(noun, vbd)
            yield template.format(noun, vbn)

            # vbn is correct
            yield template.format(noun, 'had ' + vbd)
            yield template.format(noun, 'had ' + vbn)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
