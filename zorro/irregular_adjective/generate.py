import random

NUM_ADJECTIVES = 50
NUM_NOUNS = 90

template1 = '{} {} {} {} is {} .'
template2 = '{} {} {} {} was not {} .'


def main():
    """
    example:
    "maybe the known dog is black ." vs. "maybe the know dog is black ."

    """

    from zorro.irregular_adjective.shared import paradigm, determiners
    from zorro.irregular_adjective.shared import adj_and_verb_forms
    from zorro.task_words import get_task_words
    from zorro.vocab import get_vocab_words
    from zorro import configs

    vocab = get_vocab_words()
    modifiers = ['maybe', 'i think', 'we hope that', 'he said that']
    nouns_s = get_task_words(paradigm, 'NN', 0, NUM_NOUNS)
    adjectives = get_task_words(paradigm, 'JJ', 0, NUM_ADJECTIVES)

    def gen_sentences():
        while True:

            # random choices
            noun = random.choice(nouns_s)
            det = random.choice(determiners)
            adj = random.choice(adjectives)
            mod = random.choice(modifiers)

            # get two contrasting irregular inflected forms
            adj_form, verb_form = random.choice(adj_and_verb_forms)
            if (adj_form not in vocab or verb_form not in vocab) or adj_form == verb_form:
                continue

            # adj_form is always correct.
            # we can't balance adj_form vs. verb_form because verb form requires different template

            yield template1.format(mod, det, adj_form, noun, adj)
            yield template1.format(mod, det, verb_form, noun, adj)

            yield template2.format(mod, det, adj_form, noun, adj)
            yield template2.format(mod, det, verb_form, noun, adj)

    # only collect unique sentences
    sentences = set()
    gen = gen_sentences()
    while len(sentences) // 2 < configs.Data.num_pairs_per_paradigm:
        sentence = next(gen)
        if sentence not in sentences:
            yield sentence
        sentences.add(sentence)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
