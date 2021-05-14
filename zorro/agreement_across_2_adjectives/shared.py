from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

demonstratives_singular = ["this", "that"]
demonstratives_plural = ["these", "those"]


templates = [
    'look at this/these _ _ _ ',
    'this/these _ _ _  went there',
]

nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]
