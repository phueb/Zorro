from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

pre_nominals_singular = ['this', 'that', 'one']
pre_nominals_plural = ['these', 'those', 'all']

templates = [
    '_ _ must be here',
    '_ _ can be here',
             ]

nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

