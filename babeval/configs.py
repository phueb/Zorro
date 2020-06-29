from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    predictions = Path('/') / 'media' / 'research_data' / 'BabyBertSRL' / 'runs'
    dummy_predictions = root / 'prediction_files'

    assert predictions.is_dir()
    assert dummy_predictions.is_dir()


class Eval:
    step = 180_000
    param_names = ['param_001', 'param_002', 'param_003']