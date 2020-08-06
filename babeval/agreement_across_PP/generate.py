from pathlib import Path
import random

from babeval.vocab import get_vocab


NUM_SUBJECT_NOUNS_FROM_EACH_LIST = 50  # some number smaller than length of both singular and plural noun lists
NUM_OBJECT_NOUNS_FROM_EACH_LIST = 8  # some number smaller than length of both singular and plural noun lists
NUM_ADJECTIVES = 4
NUM_PREPOSITIONS = 2

template = 'the {} {} [MASK] {} .'

nouns_plural = (Path(__file__).parent / 'word_lists' / 'nouns_plural_annotator2.txt').open().read().split()
nouns_plural = [w for w in nouns_plural if w in get_vocab()]

nouns_singular = (Path(__file__).parent / 'word_lists' / 'nouns_singular_annotator2.txt').open().read().split()
nouns_singular = [w for w in nouns_singular if w in get_vocab()]

prepositions = (Path(__file__).parent / 'word_lists' / 'prepositions_annotator2.txt').open().read().split()
prepositions = [w for w in prepositions if w in get_vocab()]

adjectives = (Path(__file__).parent / 'word_lists' / 'adjectives_annotator2.txt').open().read().split()
adjectives = [w for w in adjectives if w in get_vocab()]


def main():
    """
    example:
    "the dog on the mat [MASK] brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of plural vs. singular object nouns n singular vs. plural sentences
    3. use the same prepositional phrases for sentences with singular and plural subject nouns
    """

    random.seed(3)

    assert NUM_ADJECTIVES <= len(adjectives)
    assert NUM_PREPOSITIONS <= len(prepositions)
    assert NUM_SUBJECT_NOUNS_FROM_EACH_LIST < len(nouns_singular)
    assert NUM_SUBJECT_NOUNS_FROM_EACH_LIST < len(nouns_plural)

    nouns_subject_balanced = random.sample(nouns_singular, k=NUM_SUBJECT_NOUNS_FROM_EACH_LIST) + \
                             random.sample(nouns_plural, k=NUM_SUBJECT_NOUNS_FROM_EACH_LIST)

    nouns_object_balanced = random.sample(nouns_singular, k=NUM_OBJECT_NOUNS_FROM_EACH_LIST) + \
                            random.sample(nouns_plural, k=NUM_OBJECT_NOUNS_FROM_EACH_LIST)

    adjectives_sample = random.sample(adjectives, k=NUM_ADJECTIVES)
    prepositions_sample = random.sample(prepositions, k=NUM_PREPOSITIONS)

    prepositional_phrases = []
    for preposition in prepositions_sample:
        for noun_object in nouns_object_balanced:
            prepositional_phrase = preposition + ' ' + 'the' + ' ' + noun_object
            prepositional_phrases.append(prepositional_phrase)

    print(f'Made {len(prepositional_phrases)} prepositional phrases')

    for noun_subject in nouns_subject_balanced:
        for pp in prepositional_phrases:
            for adjective in adjectives_sample:
                yield template.format(noun_subject, pp, adjective)