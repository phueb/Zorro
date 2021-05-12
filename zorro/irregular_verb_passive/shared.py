from pathlib import Path
import spacy



nlp = spacy.load('en_core_web_sm')

paradigm = Path(__file__).parent.stem


templates = [
    'irregular adjective',
]

determiners = ['the', 'this', 'one', 'your']

vds_vns = [
    ('wore', 'worn'),
    ('broke', 'broken'),
    ('hid', 'hidden'),
    ('forgot', 'forgotten'),
    ('took', 'taken'),

    # ditransitive
    ('forbade', 'forbidden'),
    ('gave', 'given'),
]
