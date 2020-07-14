from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    runs_server = Path('/') / 'media' / 'research_data' / 'BabyBertSRL' / 'runs'
    runs_dummy = root / 'runs'


class Eval:
    dummy = True  # use files containing dummy predictions not on lab server
    step = 180_000
    param_names = ['param_002', 'param_004']
    condition = 'srl_interleaved'
    max_reps = 10
