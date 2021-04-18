import numpy as np
from typing import List

from zorro import configs
from zorro.vocab import load_vocab_df


def find_counterbalanced_subset(task_words: List[str],
                                min_size: int,
                                max_size: int,
                                num_tries_per_size: int = 10_000,
                                verbose: bool = False,
                                seed: int = configs.Data.seed,
                                ):
    """
    find subset of task words from vocab words:
     - that has an acceptable number of words (between min_size and max_size)
     - that occur in wikipedia3
     - the total frequency of which is relatively equal between:
        a) aochildes + aonewsela
        b) wikipedia1 + wikipedia2

    we use "bias" to refer to the largest word frequency difference between a) and b).

    a heuristic search is used to find such a subset.
    """

    print(f'Finding counterbalanced task word subset with min={min_size} and max={max_size}')

    corpus_names = [
        'aochildes',
        'aonewsela',
        'wikipedia1',
        'wikipedia2',
        'wikipedia3',
    ]

    np.random.seed(seed)

    if min_size <= 0:
        min_size = configs.Data.min_num_task_words_per_slot
    if max_size > len(task_words):
        max_size = len(task_words)

    vocab_df = load_vocab_df()
    f_df = vocab_df[[f'{corpus_name}-frequency' for corpus_name in corpus_names]]
    vw2fs = {w: fs.values for w, fs in f_df.iterrows()}
    print(vw2fs)

    task_words = [w for w in task_words if vw2fs[w].sum() > configs.Data.min_total_f]

    def get_total_fs(s: List[str],
                     ) -> np.array:
        fs = np.array([vw2fs[w] for w in s])
        return fs.sum(axis=0)

    def calc_bias(fs_: np.array,
                  ) -> int:
        a = fs_[0] + fs_[1]  # aochildes + aonewsela
        b = fs_[2] - fs_[3]  # wikipedia1 + wikipedia2
        res = abs(a-b)

        return res

    def rate_word(word: str,
                  ) -> float:
        """
        reward words with:
         - relatively equal corpus frequencies

        """
        fs = vw2fs[word]
        reward_equal_fs = 1 / calc_bias(fs)
        return reward_equal_fs

    # heuristic search is based on preferentially sampling words with high "rating"
    probabilities = np.array([rate_word(w) for w in task_words])
    probabilities /= probabilities.sum()

    if verbose:
        for w, p in sorted(zip(task_words, probabilities), key=lambda i: i[1]):
            print(f'{w:<24} {p:.8f} {vw2fs[w]}')

    is_found = False
    for subset_size in range(min_size, max_size):

        biases = []
        total_fs_list = []
        for _ in range(num_tries_per_size):
            sample = np.random.choice(task_words, size=subset_size, replace=False, p=probabilities)

            total_fs = get_total_fs(sample)
            total_fs_sum = total_fs.sum()
            bias = calc_bias(total_fs)
            biases.append(bias)
            total_fs_list.append(total_fs)

            is_found = bias < configs.Data.bias_tolerance

            if is_found:
                print('Found counterbalanced task-word subset:')
                if verbose:
                    for w in sample:
                        print(f"{w:<24} {vw2fs[w]}")
                print(f'Corpus frequencies={total_fs}')
                print(f'Total bias = {bias :,}')
                print(f'Total sum  = {total_fs_sum :,}')
                return sample

        if not is_found:
            idx = np.argmin(biases).item()
            print(f'size={subset_size:,}/{len(task_words):,} best: bias={biases[idx]:>12,} total_fs={str(total_fs_list[idx]):>24} sum={total_fs_list[idx].sum():>12,}')

    else:
        raise RuntimeError('No task word subset found that meets provided conditions')
