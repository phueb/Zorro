from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem


copula_singular = ["is", "was"]
copula_plural = ["are", "were"]

templates = [
    'where is/are the _ ?',
    'what is/are the _ ?',
    'is/are the _ here ?',
             ]

nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]