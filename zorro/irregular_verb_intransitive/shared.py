from pathlib import Path
import spacy


from zorro.vocab import get_vocab_words

nlp = spacy.load('en_core_web_sm')

paradigm = Path(__file__).parent.stem


templates = [
    'irregular verb intransitive',
]

determiners = ['the', 'this', 'one', 'your']

vb2vbd_vbn_intransitive = {
    'arise': ('arose', 'arisen'),
    'begin': ('began', 'begun'),
    'fall': ('fell', 'fallen'),
    'fly': ('flew', 'flown'),
    'drive': ('drove', 'driven'),
    'grow': ('grew', 'grown'),
    'hide': ('hid', 'hidden'),
    'rise': ('rose', 'risen'),
    'swear': ('swore', 'sworn'),

    # optional argument
    'drink': ('drank', 'drunk'),
    'eat': ('ate', 'eaten'),
    'draw': ('drew', 'drawn'),
    'write': ('wrote', 'written'),
    'sing': ('sang', 'sung'),
    'speak': ('spoke', 'spoken'),
    'come': ('came', 'come'),
}
