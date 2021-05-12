from pathlib import Path
import spacy



nlp = spacy.load('en_core_web_sm')

paradigm = Path(__file__).parent.stem


templates = [
    'irregular adjective',
]

determiners = ['the', 'this', 'one', 'your']

adj_and_verb_forms = [
    ('wore', 'worn'),
    ('broke', 'broken'),
    ('hid', 'hidden'),
    ('forgot', 'forgotten'),
    ('took', 'taken'),
]
