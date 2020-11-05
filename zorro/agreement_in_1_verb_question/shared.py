from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem


subjective_copula_singular = ["is", "'s", "was"]  # "do" and "does" should not be considered correct answers
subjective_copula_plural = ["are", "'re", "were"]

templates = ['template1',
             ]

nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]