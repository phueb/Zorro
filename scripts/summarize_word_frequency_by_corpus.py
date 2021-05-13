"""
How often do words in test sentences occur in each target corpus?
"""
import numpy as np

from zorro import configs
from zorro.vocab import load_vocab_df

VOCAB_SIZE = 8192

vocab_df = load_vocab_df(vocab_name=configs.Data.vocab_name_template.format(VOCAB_SIZE),
                         return_excluded_words=True)
column_names = [f'{corpus_name}-frequency' for corpus_name in configs.Data.corpus_names]
f_df = vocab_df[column_names]
vw2fs = {w: np.array([fs[k] for k in column_names]) for w, fs in f_df.iterrows()}

stop_words = set((configs.Dirs.external_words / "stopwords.txt").open().read().split())

# collect types used in test sentences
for paradigm_path in (configs.Dirs.sentences / str(VOCAB_SIZE)).glob(f'*.txt'):
    words_in_test_sentences = set()
    for w in paradigm_path.read_text().split():
        if w not in stop_words:
            words_in_test_sentences.add(w)

    fs_sum = np.zeros(len(column_names))
    for w in words_in_test_sentences:
        fs = vw2fs[w]
        fs_sum += fs

    print(paradigm_path.name)
    for cn, f in zip(column_names, fs_sum):
        print(f'{cn:.<32} {f:>12,} proportion={f/ fs_sum.sum():.2f}')