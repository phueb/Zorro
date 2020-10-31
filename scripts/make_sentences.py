from pathlib import Path
import importlib

from zorro.whole_words import get_whole_words

CHECK_IN_VOCAB = True
SECONDARY_OUT_PATH = Path('/') / 'media' / 'research_data' / 'Zorro' / 'sentences' or None

whole_words = get_whole_words()


# generate sentences for all tasks
for task_type in ['forced_choice', 'open_ended']:
    for path in Path('../zorro').glob(f'*/generate_{task_type}.py'):
        task_name = path.parent.name
        generate = importlib.import_module(f'zorro.{task_name}.generate_{task_type}')

        # check for list overlap
        for w in generate.nouns_singular:
            assert w not in generate.nouns_plural
        for w in generate.nouns_plural:
            assert w not in generate.nouns_singular

        # save each file in repository, and also on shared drive
        for out_path in [
            Path("../sentences") / task_type / f'{task_name}.txt',
            SECONDARY_OUT_PATH / task_type / f'{task_name}.txt',
        ]:
            if not out_path.parent.is_dir():
                out_path.parent.mkdir(parents=True)

            with open(out_path, 'w') as f:
                for n, sentence in enumerate(generate.main()):
                    # check
                    words_to_check = sentence.split() if CHECK_IN_VOCAB else []
                    for w in words_to_check:
                        if w == configs.Data.mask_symbol:
                            continue
                        if w not in whole_words:
                            print(f'WARNING: Not in whole_words: "{w}"')
                    # write to file
                    f.write(sentence + '\n')
                print(f'Saved {n:,} sentences to {out_path}')
