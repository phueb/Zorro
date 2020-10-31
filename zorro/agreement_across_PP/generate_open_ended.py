import random

from zorro.agreement_across_PP import *


NUM_SUBJECT_NOUNS_FROM_EACH_LIST = 50  # some number smaller than length of both singular and plural noun lists
NUM_OBJECT_NOUNS_FROM_EACH_LIST = 8  # some number smaller than length of both singular and plural noun lists
NUM_ADJECTIVES = 4
NUM_PREPOSITIONS = 2

template1 = 'the {} {}' + f' {configs.Data.mask_symbol} ' + '{} .'


def main():
    """
    example:
    "the dog on the mat [MASK] brown"

    considerations:
    1. use equal proportion of sentences containing plural vs. singular subject nouns
    2. use equal proportion of plural vs. singular object nouns n singular vs. plural sentences
    3. use the same prepositional phrases for sentences with singular and plural subject nouns
    """

    random.seed(configs.Data.seed)

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
                yield template1.format(noun_subject, pp, adjective)