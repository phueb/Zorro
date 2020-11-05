from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

templates = [
    'on the',
    'by the',
             ]

nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]