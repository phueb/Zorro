from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'ludwig_data' / 'BabyBERTa' / 'runs'
    runs_local = root / 'runs'
    data = root / 'data'
    sentences = root / 'sentences'
    external_words = data / 'external_words'
    legal_words = data / 'legal_words'


class Data:
    seed = 4
    mask_symbol = '<mask>'
    unk_symbol = '<unk>'
    space_symbol = 'Ġ'
    vocab_size = 8192
    vocab_name_template = 'wikipedia2-aonewsela-wikipedia1-aochildes-wikipedia3-{}'
    bias_tolerance = 1000  # for nouns and adjectives, but not necessarily verbs
    tag2num_words = {'NN': 50, 'JJ': 50, 'VB': 10, 'VBD': 10, 'VBG': 20}  # number of types for sampling
    min_num_words_per_slot = 20
    exclude_novel_words = False  # exclude words that do not occur at least once in each corpus?
    control_names = ['8192 frequency baseline']  #, '32768 frequency baseline']
    num_pairs_per_paradigm = 2_000
    corpus_names = [
        'aochildes',
        'aonewsela',
        'wikipedia1',
        'wikipedia2',
        'wikipedia3',
    ]


class Eval:
    local_runs = False  # use prediction files stored locally in Zorro/runs/
    steps = [0, 20_000, 40_000, 60_000, 80_000, 100_000,
             120_000, 140_000, 160_000, 180_000, 200_000,
             # 220_000, 240_000, 260_000, 280_000, 300_000,
             ]
    param_names = [f'param_{i:03}' for i in [4, 5, 6]]
    raise_error_on_missing_group = True
    conditions = ['corpora', 'load_from_checkpoint']  # can be empty list
    included_params = {}
    num_control_reps = 2
    categorize_by_template = False


class Figs:
    lw = 1
    ax_font_size = 6
    leg_font_size = 7
    dpi = 163
    title_font_size = 6
    tick_font_size = 6
