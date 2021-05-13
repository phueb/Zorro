import numpy as np
from typing import List, Optional

from zorro import configs
from zorro.vocab import load_vocab_df


def find_counterbalanced_subset(words_in_slot_: List[str],
                                min_size: int,
                                max_size: int,
                                plural_forms_: Optional[List[str]] = None,
                                num_tries_per_size: int = 100_000,
                                verbose: bool = False,
                                seed: int = configs.Data.seed,
                                ) -> List[str]:
    """
    find subset of words_in_slot from vocab words:
     - that has an acceptable number of words (between min_size and max_size)
     - that occur in wikipedia3
     - the total frequency of which is relatively equal between:
        a) aochildes + aonewsela
        b) wikipedia1 + wikipedia2

    we use "bias" to refer to the largest word frequency difference between a) and b).

    a heuristic search is used to find such a subset.
    """

    print(f'Finding counterbalanced word subset with min={min_size} and max={max_size}')

    np.random.seed(seed)

    if min_size <= 0:
        min_size = configs.Data.min_num_words_per_slot
    if max_size > len(words_in_slot_):
        max_size = len(words_in_slot_)

    vocab_df = load_vocab_df()
    column_names = [f'{corpus_name}-frequency' for corpus_name in configs.Data.corpus_names]
    f_df = vocab_df[column_names]
    vw2fs = {w: np.array([fs[k] for k in column_names]) for w, fs in f_df.iterrows()}

    # remove words if their plural is not in vocab
    words_in_slot = []
    plural_forms = []
    if plural_forms_ is not None:
        assert len(plural_forms_) == len(words_in_slot_)
        for w, plural_form in zip(words_in_slot_, plural_forms_):
            if plural_form in vw2fs:
                words_in_slot.append(w)
                plural_forms.append(w)
        assert len(plural_forms) == len(words_in_slot)
    else:
        words_in_slot = words_in_slot_
        plural_forms = plural_forms_

    def get_total_fs(s: List[str],
                     ) -> np.array:
        fs = np.array([vw2fs[w] for w in s])
        return fs.sum(axis=0)

    def calc_bias(fs_: np.array,
                  ) -> int:
        a = fs_[0] + fs_[1]  # aochildes + aonewsela
        b = fs_[2] + fs_[3]  # wikipedia1 + wikipedia2
        res = abs(a-b)

        return res

    def rate_word(word: str,
                  ) -> float:
        """
        reward words with:
         - high aochildes frequency
         - high aonewsela frequency

        """
        fs = vw2fs[word]
        term1 = np.log10(fs[0] + 1)
        term2 = np.log10(fs[1] + 1)
        return term1 * term2

    # heuristic search is based on preferentially sampling words with high "rating"
    if plural_forms is None:
        ratings = np.array([rate_word(w) for w in words_in_slot])
    else:
        ratings = np.array([rate_word(w1) * rate_word(w2) for w1, w2 in zip(words_in_slot, plural_forms)])
    probabilities = ratings / ratings.sum()

    if verbose:
        for w, p in sorted(zip(words_in_slot, probabilities), key=lambda i: i[1]):
            print(f'{w:<24} {p:.8f} {vw2fs[w]}')

    is_found = False
    for subset_size in range(min_size, max_size):

        biases = []
        total_fs_list = []
        for _ in range(num_tries_per_size):
            # get a sample of words
            sample_ids = np.random.choice(len(words_in_slot), size=subset_size, replace=False, p=probabilities)
            sample = [words_in_slot[i] for i in sample_ids]

            # compute the bias of the sample
            total_fs = get_total_fs(sample)
            if plural_forms is not None:
                total_fs += get_total_fs([plural_forms[i] for i in sample_ids])
            total_fs_sum = total_fs.sum()
            bias = calc_bias(total_fs)

            # collect bias
            biases.append(bias)
            total_fs_list.append(total_fs)

            is_found = bias < configs.Data.bias_tolerance

            if is_found:
                print('Found counterbalanced word subset:')
                if verbose:
                    for w in sample:
                        print(f"{w:<24} {vw2fs[w]}")
                print(f'Corpus frequencies={total_fs} Total bias={bias :,} Total sum={total_fs_sum :,} size={subset_size:,}')
                return sample

        if not is_found:
            idx = np.argmin(biases).item()
            print(f'size={subset_size:,}/{len(words_in_slot):,} best: bias={biases[idx]:>12,} total_fs={str(total_fs_list[idx]):>24} sum={total_fs_list[idx].sum():>12,}')

    else:
        raise RuntimeError('No word subset found that meets provided conditions')
