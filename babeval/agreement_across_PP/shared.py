from pathlib import Path
import inflect

plural = inflect.engine()

task_name = Path(__file__).parent.stem

copulas_singular = ["is", "'s", "was"]
copulas_plural = ["are", "'re", "were"]

templates = [
    'on the',
    'by the',
             ]

