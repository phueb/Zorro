from pathlib import Path


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
    'allen',
]


vbds_vbns_transitive = [
    # transitive
    ('was', 'been'),
    ('bore', 'borne'),
    ('beat', 'beaten'),
    ('became', 'become'),
    ('bit', 'bitten'),
    ('blew', 'blown'),
    ('chose', 'chosen'),
    ('did', 'done'),
    ('forgave', 'forgiven'),
    ('rode', 'ridden'),
    ('shook', 'shaken'),
    ('strode', 'stridden'),
    ('took', 'taken'),
    ('threw', 'thrown'),

    # optional
    ('knew', 'known'),
    ('saw', 'seen'),
]
