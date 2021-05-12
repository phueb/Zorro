from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem


copulas_singular = ["is", "was"]
copulas_plural = ["are", "were"]

templates = [
    'where is/are the _ ?',
    'what is/are the _ ?',
    'what is/are wrong with the _ ?',
    'is/are the _ not _ ?',
    'is/are the _ where it should be ?',
    'is/are the _ where they should be ?',
    'is/are the _ something you like ?',
    'is/are the _ a good idea ?',
             ]

nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]