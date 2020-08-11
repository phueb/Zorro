from pathlib import Path
import importlib


# generate sentences for all tasks
for task_type in ['forced_choice', 'open_ended']:
    for path in Path('babeval').glob(f'*/generate_{task_type}.py'):
        task_name = path.parent.name
        generate = importlib.import_module(f'babeval.{task_name}.generate_{task_type}')

        out_path = Path("sentences") / task_type / f'{task_name}.txt'
        with open(out_path, 'w') as f:
            for n, sentence in enumerate(generate.main()):
                f.write(sentence + '\n')
            print(f'Saved {n:,} sentences to {out_path}')
