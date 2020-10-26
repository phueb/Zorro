from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'research_data' / 'BabyBert' / 'runs'
    runs_local = root / 'runs'
    data = root / 'data'
    word_lists = data / 'word_lists'


class Data:
    vocab_path = '/home/ph/BabyBERT/data/tokenizers/c-n-w-8192/vocab.json'
    corpora_path = '/home/ph/BabyBERT/data/corpora'
    annotator = 'annotator_2'
    seed = 3

    control_name_1gram = '1-gram-distribution control'
    control_name_left_2gram = 'left 2-gram-distribution control'
    control_name_right_2gram = 'right 2-gram-distribution control'
    control_names = [control_name_1gram, control_name_left_2gram, control_name_right_2gram]


class Eval:
    local_runs = False  # use prediction files fom this repository
    custom_steps = [180_000]  # or None  or [-1] to indicate last available step
    param_names = [f'param_00{i}' for i in [1, 6, 7, 5, 8]]
    raise_error_on_missing_group = True
    conditions = ['bbpe']  # can be empty list
    max_reps = 10
    num_control_reps = 2
