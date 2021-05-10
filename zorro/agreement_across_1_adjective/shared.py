from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]

templates = [
    'look at this/these _ _',
    'this/these _ _  went there',
]

nouns_singular = get_task_words(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]
