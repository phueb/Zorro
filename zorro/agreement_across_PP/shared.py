from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

copulas_singular = ["is", "was"]
copulas_plural = ["are", "were"]

templates = [
    'on the',
    'by the',
             ]

nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]
