from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'ludwig_data' / 'BabyBERTa' / 'runs'
    runs_local = root / 'runs'
    data = root / 'data'
    external_words = data / 'external_words'
    task_words = data / 'task_words'


class Data:
    seed = 4
    mask_symbol = '<mask>'
    unk_symbol = '<unk>'
    space_symbol = 'Ġ'
    vocab_name = 'wikipedia2-aonewsela-wikipedia1-aochildes-wikipedia3'
    min_total_f = 10  # a task word must occur at least this number of times across all corpora
    bias_tolerance = 1000
    min_num_task_words_per_slot = 20
    exclude_novel_words = False  # exclude words that do not occur at least once in each corpus?
    control_name_1gram = 'word-frequency control'
    control_names = [control_name_1gram]


class Eval:
    local_runs = False  # use prediction files stored locally in Zorro/runs/
    steps = [i for i in range(0, 200_000, 20_000)]  # [180_000]  # or [-1] to indicate last available step
    param_names = [f'param_{i:03}' for i in [1, 2]]
    raise_error_on_missing_group = True
    conditions = ['corpora', 'leave_unmasked_prob_start']  # can be empty list
    included_params = {}
    max_reps = 10
    num_control_reps = 2


class Figs:
    lw = 1
    ax_font_size = 14
    leg_font_size = 8
    dpi = 163
    title_font_size = 8
    tick_font_size = 8