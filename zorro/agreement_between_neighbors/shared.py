from pathlib import Path
import inflect

from zorro.task_words import get_task_words

plural = inflect.engine()

task_name = Path(__file__).parent.stem

pre_nominals_singular = ['this', 'that', 'one']
pre_nominals_plural = ['these', 'those', 'all']

templates = [
    '_ _ must be here',
    '_ _ can be here',
             ]

nouns_singular = get_task_words(task_name, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

