from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = ['template1',
             ]

nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

