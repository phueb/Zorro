"""
generate sentences for all paradigms.
"""
from pathlib import Path
import importlib

from zorro.vocab import get_vocab_words
from zorro import configs

CHECK_IN_VOCAB = True
VOCAB_SIZES = [8192, 32768]
# VOCAB_SIZES = [8192, 16384, 32768]
SECONDARY_OUT_PATH = Path('/') / 'media' / 'ludwig_data' / 'Zorro' / 'sentences' or None

stop_words = (configs.Dirs.external_words / "stopwords.txt").open().read().split()
nas = (configs.Dirs.external_words / "nouns_ambiguous_number.txt").open().read().split()

# for all vocab sizes
for vocab_size in VOCAB_SIZES:

    print('**********************************************')
    print(f'Making test sentences with vocab size={vocab_size}')
    print('**********************************************')

    configs.Data.vocab_size = vocab_size
    vocab_words = get_vocab_words()

    # for all paradigms
    for path in sorted(Path('../zorro').glob(f'*/generate.py')):
        paradigm = path.parent.name

        try:
            generate = importlib.import_module(f'zorro.{paradigm}.generate')
            shared = importlib.import_module(f'zorro.{paradigm}.shared')
        except RuntimeError as e:
            print(e)
            print(f'Skipping {paradigm}')
            continue

        # generate sentences once, in order to save the same sentences to two locations
        sentences = list(generate.main())

        # save each file in repository, and also on shared drive
        for out_path in [
            Path("../sentences") / str(vocab_size) / f'{paradigm}.txt',
            SECONDARY_OUT_PATH / 'forced_choice' / str(vocab_size) / f'{paradigm}.txt',
        ]:
            if not out_path.parent.is_dir():
                out_path.parent.mkdir(parents=True)

            num_saved_sentences = 0
            with open(out_path, 'w') as f:
                for sentence in sentences:
                    # check
                    words_to_check = sentence.split() if CHECK_IN_VOCAB else []
                    for w in words_to_check:
                        if w == configs.Data.mask_symbol:
                            continue
                        if w not in vocab_words and w not in stop_words:
                            print(f'WARNING: Not in whole_words or stop words: "{w}"')
                        if w in nas:
                            print(f'WARNING: Found noun with ambiguous number: "{w}"')
                    # write to file
                    f.write(sentence + '\n')
                    num_saved_sentences += 1

            if not num_saved_sentences:
                raise RuntimeError('Task did not generate any sentences.'
                                   'This can occur if plural versions of singular nouns are not in vocab.')
            print(f'Saved {num_saved_sentences:>12,} sentences to {out_path}')
