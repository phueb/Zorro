from pathlib import Path

paradigm = Path(__file__).parent.stem


templates = [
    'irregular verb intransitive',
]

determiners = ['the', 'this', 'one', 'your']

vbds_vbns_intransitive = [
    ('arose', 'arisen'),
    ('began', 'begun'),
    ('fell', 'fallen'),
    ('flew', 'flown'),
    ('drove', 'driven'),
    ('grew', 'grown'),
    ('hid', 'hidden'),
    ('rose', 'risen'),
    ('swore', 'sworn'),

    # optional argument
    ('drank', 'drunk'),
    ('ate', 'eaten'),
    ('drew', 'drawn'),
    ('wrote', 'written'),
    ('sang', 'sung'),
    ('spoke', 'spoken'),
    ('came', 'come'),
]
