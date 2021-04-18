"""
generate sentences for all tasks.
"""

from pathlib import Path
import importlib

from zorro.vocab import get_vocab_words
from zorro import configs

CHECK_IN_VOCAB = True
SKIP_OPEN_ENDED = True
SECONDARY_OUT_PATH = Path('/') / 'media' / 'ludwig_data' / 'Zorro' / 'sentences' or None

vocab_words = get_vocab_words()

stop_words = (configs.Dirs.external_words / "stopwords.txt").open().read().split()
nas = (configs.Dirs.external_words / "nouns_ambiguous_number.txt").open().read().split()

# for all task types
for task_type in ['forced_choice', 'open_ended']:

    if SKIP_OPEN_ENDED and task_type == 'open_ended':
        continue

    # for all tasks with given type
    for path in sorted(Path('../zorro').glob(f'*/generate_{task_type}.py')):
        task_name = path.parent.name
        try:
            generate = importlib.import_module(f'zorro.{task_name}.generate_{task_type}')
            shared = importlib.import_module(f'zorro.{task_name}.shared')
        except RuntimeError as e:
            print(e)
            print(f'Skipping {task_name}')
            continue

        # save each file in repository, and also on shared drive
        for out_path in [
            Path("../sentences") / task_type / f'{task_name}.txt',
            SECONDARY_OUT_PATH / task_type / f'{task_name}.txt',
        ]:
            if not out_path.parent.is_dir():
                out_path.parent.mkdir(parents=True)

            num_saved_sentences = 0
            with open(out_path, 'w') as f:
                for sentence in generate.main():
                    # check
                    words_to_check = sentence.split() if CHECK_IN_VOCAB else []
                    for w in words_to_check:
                        if w == configs.Data.mask_symbol:
                            continue
                        if w not in vocab_words and w not in stop_words:
                            print(f'WARNING: Not in whole_words or stop words: "{w}"')
                    # write to file
                    f.write(sentence + '\n')
                    num_saved_sentences += 1

            if not num_saved_sentences:
                raise RuntimeError('Task did not generate any sentences.'
                                   'This can occur if plural versions of singular nouns are not in vocab.')
            print(f'Saved {num_saved_sentences:>12,} sentences to {out_path}')
