from pathlib import Path

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
