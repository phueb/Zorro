from pathlib import Path
import spacy


from zorro.vocab import get_vocab_words

nlp = spacy.load('en_core_web_sm')

task_name = Path(__file__).parent.stem


templates = [
    'intransitive',
    'transitive-optional',
    'transitive',
]

determiners = ['the', 'this', 'one', 'your']

verbs_base = get_vocab_words(tag='VB')
# names = get_vocab_words(tag='NNP')  # TODO test


vb2vbd_vbn_intransitive = {
    'arise': ('arose', 'arisen'),
    'begin': ('began', 'begun'),
    'fall': ('fell', 'fallen'),
    'fly': ('flew', 'flown'),
    'drive': ('drove', 'driven'),
    'grow': ('grew', 'grown'),
    'hide': ('hid', 'hidden'),
    'rise': ('rose', 'risen'),
}

vb2vbd_vbn_optional = {
    'drink': ('drank', 'drunk'),
    'eat': ('ate', 'eaten'),
    'draw': ('drew', 'drawn'),
    'know': ('knew', 'known'),
    'see': ('saw', 'seen'),
    'write': ('wrote', 'written'),
    'swear': ('swore', 'sworn'),
    'sing': ('sang', 'sung'),
    'speak': ('spoke', 'spoken'),
    'come': ('came', 'come'),
}

vb2vbd_vbn_transitive = {
    # transitive
    'be': ('was', 'been'),
    'bear': ('bore', 'borne'),
    'beat': ('beat', 'beaten'),
    'become': ('became', 'become'),
    'bite': ('bit', 'bitten'),
    'blow': ('blew', 'blown'),
    'build': ('built', 'brought'),
    'choose': ('chose', 'chosen'),
    'do': ('did', 'done'),
    'forgive': ('forgave', 'forgiven'),
    'ride': ('rode', 'ridden'),
    'shake': ('shook', 'shaken'),
    'stride': ('strode', 'stridden'),
    'take': ('took', 'taken'),
    'throw': ('threw', 'thrown'),
}
vb2vbd_vbn_ditransitive = {
    # ditransitive
    'forbid': ('forbade', 'forbidden'),
    'give': ('gave', 'given'),
}
