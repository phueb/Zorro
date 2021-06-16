"""
generate sentences for all paradigms.
"""
from pathlib import Path
import importlib

from zorro.vocab import get_vocab_words
from zorro.filter import collect_unique_pairs
from zorro.utils import get_phenomena_and_paradigms, capitalize_names_in_sentence
from zorro import configs

SECONDARY_OUT_PATH = Path('/') / 'media' / 'ludwig_data' / 'Zorro' / 'sentences' or None

stop_words = (configs.Dirs.external_words / "stopwords.txt").open().read().split()
number_words = (configs.Dirs.legal_words / "number_words.txt").open().read().split()

vocab_words = get_vocab_words()

# for all paradigms
for phenomenon, paradigm in get_phenomena_and_paradigms():

    print('***************************************************************************************')
    print(f'Making test sentences for {phenomenon} {paradigm} with vocab={configs.Data.vocab_name}')
    print('***************************************************************************************')

    try:
        paradigm_module = importlib.import_module(f'zorro.{phenomenon}.{paradigm}')
    except RuntimeError as e:
        print(e)
        print(f'Skipping {paradigm}')
        continue

    # generate sentences once, in order to save the same sentences to two locations
    sentences = list(collect_unique_pairs(paradigm_module.main))
    assert sentences

    # capitalize proper nouns for case-sensitive models like roberta-base
    sentences = [capitalize_names_in_sentence(s) for s in sentences]

    # TODO save info about each sentence's template in the text file saved locally

    # save each file in repository, and also on shared drive
    for out_path in [
        Path("../sentences") / configs.Data.vocab_name / f'{phenomenon}-{paradigm}.txt',
        SECONDARY_OUT_PATH / configs.Data.vocab_name / f'{phenomenon}-{paradigm}.txt',
    ]:
        if not out_path.parent.is_dir():
            out_path.parent.mkdir(parents=True)

        num_saved_sentences = 0
        with open(out_path, 'w') as f:
            for sentence in sentences:
                # check
                words_to_check = sentence.split()
                for w in words_to_check:
                    if w.lower() not in vocab_words and w.lower() not in stop_words:
                        raise RuntimeError(f'WARNING: Not a whole word and not a stop word: "{w}"')
                # write to file
                f.write(sentence + '\n')
                num_saved_sentences += 1

        if not num_saved_sentences:
            raise RuntimeError('Did not generate any sentences.'
                               'This can occur if plural versions of singular nouns are not in vocab.')
        print(f'Saved {num_saved_sentences:>12,} sentences to {out_path}')
