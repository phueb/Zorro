from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

copulas_singular = ["is", "was"]
copulas_plural = ["are", "were"]

templates = [
    'on the',
    'by the',
             ]

nouns_singular = get_task_words(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]
