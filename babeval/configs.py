from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'research_data' / 'BabyBert' / 'runs'
    runs_local = root / 'runs'


class Data:
    annotator = 'annotator_2'
    seed = 3
    control_name_1gram = '1-gram-distribution control'
    control_name_left_2gram = 'left 2-gram-distribution control'
    control_name_right_2gram = 'right 2-gram-distribution control'
    control_names = [control_name_1gram, control_name_left_2gram, control_name_right_2gram]
    num_control_reps = 2


class Eval:
    local_runs = False  # use prediction files fom this repository
    custom_steps = [-1]  # or None  or [-1] to indicate last available step
    param_names = None  # ['BERT_MEDIUM_AUG24', 'BERT_MEDIUM_WWM', 'param_001']
    raise_error_on_missing_group = True
    condition = 'num_utterances_per_input'
    max_reps = 10
