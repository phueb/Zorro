"""
How often do words in test sentences occur in each target corpus?
"""
import numpy as np

from zorro import configs
from zorro.vocab import load_vocab_df

vocab_df = load_vocab_df(return_excluded_words=True)
column_names = [f'{corpus_name}-frequency' for corpus_name in configs.Data.corpus_names]
f_df = vocab_df[column_names]
vw2fs = {w: np.array([fs[k] for k in column_names]) for w, fs in f_df.iterrows()}

stop_words = set((configs.Dirs.external_words / "stopwords.txt").open().read().split())

# collect types used in test sentences
cn2f = {cn: 0 for cn in column_names}
fs_sum_total = 0
for paradigm_path in (configs.Dirs.sentences / 'babyberta').glob('*.txt'):
    words_in_test_sentences = set()
    for w in paradigm_path.read_text().split():
        if w not in stop_words:
            words_in_test_sentences.add(w.lower())

    fs_sum = np.zeros(len(column_names))
    for w in words_in_test_sentences:
        fs = vw2fs[w]
        fs_sum += fs

    # collect
    fs_sum_total += fs_sum.sum()
    print(fs_sum_total)

    print(paradigm_path.name)
    for cn, f in zip(column_names, fs_sum):
        print(f'{cn:.<32} {f:>12,} proportion={f/ fs_sum.sum():.2f}')

        # collect
        cn2f[cn] += f

# summary
print()
print('Summary')
for cn, f in cn2f.items():
    print(f'{cn:.<32} {f:>12,} proportion={f/ fs_sum_total:.3f}')