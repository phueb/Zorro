from pathlib import Path
import inflect

plural = inflect.engine()

task_name = Path(__file__).parent.stem

pre_nominals_singular = ["this", "that"]
pre_nominals_plural = ["these", "those"]
pre_nominals = set(pre_nominals_singular + pre_nominals_plural)

templates = [
    'look at ...',
    '... went there',
]
