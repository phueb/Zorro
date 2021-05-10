from pathlib import Path
import inflect

from zorro.task_words import get_task_words

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

adjectives = get_task_words(paradigm, 'JJ')
nouns_singular = get_task_words(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

