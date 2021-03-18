"""
Find set of words such that that the sum of their corpus frequencies are as close possible to each other.
"""
import numpy as np

from zorro.vocab import load_vocab_df

MIN_SUBSET_SIZE = 200
MAX_SUBSET_SIZE = 300
MIN_WORD_FREQUENCY = 10
POS = 'NN'
MIN_TOTAL_FREQUENCY = 100_000
BIAS_TOLERANCE = 1_000
VERBOSE = False
NUM_TRIES = 10_000


def score_probability(word: str):
    """assign a score to a word, such that larger score indicates word frequencies are biased toward bias pattern"""
    fs = get_word_pattern(word)
    bias = calc_bias(fs)
    reward_large_f = np.log(fs.sum())
    reward_equal_fs = 1 / bias
    return reward_equal_fs * reward_large_f


def get_word_pattern(word):
    return np.array([word2data[word][n] for n in f_col_names])


def calc_bias(total_fs_):
    diff1 = total_fs_[0] - total_fs_[1]
    diff2 = total_fs_[0] - total_fs_[2]
    diff3 = total_fs_[1] - total_fs_[2]
    res = max([abs(diff1), abs(diff2), abs(diff3)])

    return res


def get_total_fs(s):
    fs = np.array([[word2data[word][n] for n in f_col_names]
                   for word in s])
    return fs.sum(axis=0)


vocab_df = load_vocab_df()
word2data = vocab_df.to_dict('index')
vocab_words = [w for w in vocab_df.index.tolist()
               if not word2data[w]['is_excluded'] and
               word2data[w][POS] > 0 and word2data[w]['total-frequency'] > MIN_WORD_FREQUENCY]

f_col_names = [f'{initial}-frequency' for initial in ['c', 'n', 'w']]

probabilities = np.array([score_probability(w) for w in vocab_words])
probabilities /= probabilities.sum()

for w, p in sorted(zip(vocab_words, probabilities), key=lambda i: i[1]):
    print(f'{w:<24} {p:.8f} {get_word_pattern(w)}')


is_ok = False
for subset_size in range(MIN_SUBSET_SIZE, MAX_SUBSET_SIZE):
    print(f'Finding subset of size {subset_size:,} for vocab of size {len(vocab_words):,}...')

    biases = []
    total_fs_list = []
    for _ in range(NUM_TRIES):
        sample = np.random.choice(vocab_words, size=subset_size, replace=False, p=probabilities)

        total_fs = get_total_fs(sample)
        total_fs_sum = total_fs.sum()
        bias = calc_bias(total_fs)
        biases.append(bias)
        total_fs_list.append(total_fs)

        is_ok = bias < BIAS_TOLERANCE and total_fs_sum > MIN_TOTAL_FREQUENCY

        if is_ok:
            print('Found subset:')
            for w in sample:
                print(f"{w:<24} {get_word_pattern(w)}")
            print(f'Corpus frequencies={total_fs}')
            print(f'Total bias = {bias :,}')
            print(f'Total sum  = {total_fs_sum :,}')
            break

    if is_ok:
        break
    else:
        idx = np.argmin(biases).item()
        print(f'Smallest bias={biases[idx]:,} best total_fs={total_fs_list[idx]} sum={total_fs_list[idx].sum():,}')


else:
    raise SystemExit('No subset found')