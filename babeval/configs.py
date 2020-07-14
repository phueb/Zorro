from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    predictions = Path('/') / 'media' / 'research_data' / 'BabyBertSRL' / 'runs'
    dummy_predictions = root / 'prediction_files'


class Eval:
    dummy = False  # use files containing dummy predictions not on lab server
    step = 180_000
    param_names = ['param_002', 'param_004']
    condition = 'srl_interleaved'
    max_reps = 2
