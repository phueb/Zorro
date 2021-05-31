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
    tag2num_words = {'NN': 50, 'JJ': 50, 'VB': 10, 'VBD': 10, 'VBG': 20, 'VBZ': 20}  # number of types for sampling
    min_num_words_per_slot = 20
    exclude_novel_words = False  # exclude words that do not occur at least once in each corpus?
    num_pairs_per_paradigm = 2_000
    corpus_names = [
        'aochildes',
        'aonewsela',
        'wikipedia1',
        'wikipedia2',
        'wikipedia3',
    ]


class Eval:
    included_params = {}
    categorize_by_template = False
    excluded_paradigms = [
        'existential_there_2',  # too difficult
        'across_2_adjectives',  # very similar performance to across_1_adjective
    ]
    local_runs = False  # use model output stored locally in Zorro/runs/

    # exp1 (part of experiment that is comparing unmasking only)
    # steps = [i for i in range(0, 180_000, 20_000)]
    # param_names = [f'param_{i:03}' for i in [1, 4]]
    # conditions = ['corpora', 'leave_unmasked_prob']
    # exp2
    steps = [i for i in range(0, 180_000, 20_000)]
    param_names = [f'param_{i:03}' for i in [1, 2, 3]]
    conditions = ['corpora', ]
    # exp3
    # steps = [i for i in range(0, 180_000, 20_000)]
    # param_names = [f'param_{i:03}' for i in [11, 13]]
    # conditions = ['corpora', 'load_from_checkpoint']
    # # exp4a
    # steps = [i for i in range(0, 500_000, 20_000)]
    # param_names = [f'param_{i:03}' for i in [20, 21, 22]]
    # conditions = ['leave_unmasked_prob_start', 'leave_unmasked_prob']
    # # exp4b
    # steps = [i for i in range(0, 500_000, 20_000)]
    # param_names = [f'param_{i:03}' for i in [23, 24]]
    # conditions = ['corpora']


class Figs:
    lw = 1
    ax_font_size = 6
    leg_font_size = 6
    title_font_size = 6
    tick_font_size = 6
