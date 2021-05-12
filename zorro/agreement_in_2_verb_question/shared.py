from pathlib import Path
import inflect

from zorro.words import get_words_for_paradigm

plural = inflect.engine()

paradigm = Path(__file__).parent.stem

doing_singular = ["does"]  # only "do" and does should be considered answers
doing_plural = ["do"]
doing_ambiguous = ["did"]

templates = [
    'where _ the _ go ?',
    'what _ the _ do ?',
    'how _ the _ fit in here ?',
    'how _ the _ become _ ?',
    'when _ the _ stop working ?',
    'when _ the _ start ?',
             ]

# load words
nouns_singular = get_words_for_paradigm(paradigm, 'NN')
nouns_plural = [plural.plural(n) for n in nouns_singular]

