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
    vocab_name = 'c-w-n'
    frequency_difference_tolerance = 1000
    control_name_1gram = 'word-frequency control'
    control_names = [control_name_1gram]


class Eval:
    local_runs = False  # use prediction files stored locally in Zorro/runs/
    steps = [-1]  # or [-1] to indicate last available step
    param_names = [f'param_{i:03}' for i in [14, 15, 16, 11, 12, 13]]
    raise_error_on_missing_group = True
    conditions = ['max_num_tokens_in_sequence', 'allow_truncated_sentences', 'corpus_name']  # can be empty list
    max_reps = 10
    num_control_reps = 2
