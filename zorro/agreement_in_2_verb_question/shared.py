from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem

doing_singular = ["does"]  # only "do" and does should be considered answers
doing_plural = ["do"]
doing_ambiguous = ["did"]

templates = ['template1',
             ]

# load task words
nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

