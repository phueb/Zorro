from pathlib import Path
import spacy


from zorro.vocab import get_vocab_words

nlp = spacy.load('en_core_web_sm')

paradigm = Path(__file__).parent.stem


templates = [
    'irregular verb transitive',
]

determiners = ['the', 'this', 'one', 'your']

names = [
    'michael',
    'simon',
    'allen',
    'obama',
    'donald',
    'henry',
    'robert',
    'bill',
    'thomas',
    'mark',
    'richard',
    'louis',
    'joseph',
    'edward',
    'sarah',
    'laura',
    'santa',
]


vb2vbd_vbn_transitive = {
    # transitive
    'be': ('was', 'been'),
    'bear': ('bore', 'borne'),
    'beat': ('beat', 'beaten'),
    'become': ('became', 'become'),
    'bite': ('bit', 'bitten'),
    'blow': ('blew', 'blown'),
    'choose': ('chose', 'chosen'),
    'do': ('did', 'done'),
    'forgive': ('forgave', 'forgiven'),
    'ride': ('rode', 'ridden'),
    'shake': ('shook', 'shaken'),
    'stride': ('strode', 'stridden'),
    'take': ('took', 'taken'),
    'throw': ('threw', 'thrown'),

    # optional
    'know': ('knew', 'known'),
    'see': ('saw', 'seen'),


}
vb2vbd_vbn_ditransitive = {
    # ditransitive
    'forbid': ('forbade', 'forbidden'),
    'give': ('gave', 'given'),
}
