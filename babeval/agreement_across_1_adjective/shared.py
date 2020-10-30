from pathlib import Path
import inflect

from babeval.task_words import get_task_word_combo

plural = inflect.engine()

task_name = Path(__file__).parent.stem

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]

templates = [
    'look at ...',
    '... went there',
]

noun_plurals = get_task_word_combo