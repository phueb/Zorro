from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'research_data' / 'BabyBert' / 'runs'
    runs_local = root / 'runs'
    data = root / 'data'
    external_words = data / 'external_words'
    task_words = data / 'task_words'


class Data:
    vocab_path = '/home/ph/BabyBERT/data/tokenizers/c-n-w-8192/vocab.json'
    corpora_path = '/home/ph/BabyBERT/data/corpora'
    seed = 3
    mask_symbol = '<mask>'
    unk_symbol = '<unk>'
    space_symbol = 'Ġ'
    ww_name = 'c-w-n'

    control_name_1gram = '1-gram-distribution control'
    control_names = [control_name_1gram]


class Eval:
    local_runs = True  # use prediction files fom this repository
    custom_steps = [-1]  # or [-1] to indicate last available step
    param_names = None  # [f'param_00{i}' for i in [1, 6, 7, 5, 8]]
    raise_error_on_missing_group = True
    conditions = ['architecture']  # can be empty list
    max_reps = 10
    num_control_reps = 2
