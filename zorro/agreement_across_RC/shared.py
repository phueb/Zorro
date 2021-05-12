from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

copulas_singular = ["is", "was"]
copulas_plural = ["are", "were"]

pronouns_1p_2p = ['i', 'you', 'we']
pronouns_3p = ['he', 'she', 'it']
assert len(pronouns_3p) == len(pronouns_1p_2p)

templates = [
    'object-relative',
    'subject-relative',
]

adjectives = get_words_for_paradigm(paradigm, 'JJ')
nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

