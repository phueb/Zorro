from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_remote = Path('/') / 'media' / 'research_data' / 'BabyBertSRL' / 'runs'
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
    dummy = True  # use files containing dummy predictions not on lab server
    custom_steps = [180_000]  # used for external bert models  # or NOne
    param_names = ['BERT_MINI_CHILDES', 'BERT_MEDIUM_CHILDES', 'BERT_BASE_CHILDES'] + ['param_001', 'param_002']
    raise_error_on_missing_group = False
    condition = 'srl_interleaved'
    max_reps = 10
