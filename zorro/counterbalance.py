import numpy as np
from typing import List

from zorro import configs
from zorro.vocab import load_vocab_df


def calc_bias(total_fs_: np.array,
              ) -> int:
    diff1 = total_fs_[0] - total_fs_[1]
    diff2 = total_fs_[0] - total_fs_[2]
    diff3 = total_fs_[1] - total_fs_[2]
    res = max([abs(diff1), abs(diff2), abs(diff3)])

    return res


def find_counterbalanced_subset(task_words: List[str],
                                min_size: int,
                                max_size: int,
                                num_tries_per_size: int = 10_000,
                                verbose: bool = False,
                                seed: int = configs.Data.seed,
                                ):
    """
    find subset of task words that:
     - has an acceptable number of words (between min_size and max_size)
     - results in bias (largest word frequency difference between any two corpora) less than some tolerance.

    a heuristic search is used to find subset
    """

    np.random.seed(seed)

    if min_size <= 0:
        min_size = configs.Data.min_num_task_words_per_slot
    if max_size > len(task_words):
        max_size = len(task_words)

    vocab_df = load_vocab_df()
    f_df = vocab_df.filter(regex='^.-frequency', axis=1)
    vw2fs = {w: fs.values for w, fs in f_df.iterrows()}

    cf_df = vocab_df['c-frequency']
    vw2cf = cf_df.to_dict()

    task_words = [w for w in task_words if vw2fs[w].sum() > configs.Data.min_total_f]

    def get_total_fs(s: List[str],
                     ) -> np.array:
        fs = np.array([vw2fs[w] for w in s])
        return fs.sum(axis=0)

    def rate_word(word: str,
                          ) -> float:
        """
        reward words with:
         - equal corpus frequencies
         - large c-frequency
        """
        fs = vw2fs[word]
        reward_equal_fs = 1 / calc_bias(fs)
        reward_large_cf = np.log(vw2cf[word] + 1)
        return reward_equal_fs * reward_large_cf

    # heuristic search is based on preferentially sampling words with high "probability"
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

            is_found = bias < configs.Data.frequency_difference_tolerance

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
