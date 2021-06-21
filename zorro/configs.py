from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs = Path('/') / 'media' / 'ludwig_data' / 'BabyBERTa' / 'runs'
    reference = root / 'reference'
    data = root / 'data'
    sentences = root / 'sentences'
    external_words = data / 'external_words'
    legal_words = data / 'legal_words'


class Data:
    seed = 4
    mask_symbol = '<mask>'
    unk_symbol = '<unk>'
    space_symbol = 'Ġ'
    vocab_name = 'babyberta'  # we use the vocab defined by babyberta model as default
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
    categorize_by_template = False
    excluded_paradigms = [
        'existential_there_2',  # too difficult
        'across_2_adjectives',  # very similar performance to across_1_adjective
        'possessive_pronoun',  # sometimes both sentences are grammatical
        'verb_in_passive_voice',  # not in BLiMP and redundant with other other "irregular" paradigm
    ]


class Figs:
    lw = 1
    ax_font_size = 6
    leg_font_size = 6
    title_font_size = 6
    tick_font_size = 6
    legend_offset_from_bottom = 0.15

