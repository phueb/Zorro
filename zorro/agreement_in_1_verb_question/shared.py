from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

paradigm = Path(__file__).parent.stem


copulas_singular = ["is", "was"]
copulas_plural = ["are", "were"]

templates = [
    'where is/are the _ ?',
    'what is/are the _ ?',
    'what is/are wrong with the _ ?',
    'is/are the _ where here ?',
    'is/are the _ where it should be ?',
    'is/are the _ where they should be ? ?',
             ]

nouns_singular = get_task_words(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]