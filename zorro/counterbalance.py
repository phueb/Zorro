import numpy as np
from typing import List, Optional, Tuple, Union

from zorro import configs
from zorro.vocab import load_vocab_df

vocab_df = load_vocab_df()
column_names = [f'{corpus_name}-frequency' for corpus_name in configs.Data.corpus_names]
f_df = vocab_df[column_names]
vw2fs = {w: np.array([fs[k] for k in column_names]) for w, fs in f_df.iterrows()}


def get_total_fs(s: List[str],
                 ) -> np.array:
    fs = np.array([vw2fs[w] for w in s])
    return fs.sum(axis=0)


def calc_bias(fs_: np.array,
              ) -> int:
    bias2 = abs(fs_[2] - fs_[0])  # aochildes vs wikipedia1
    res = bias2

    return res


def rate_word(word: str,
              ) -> float:
    """
    reward words with:
     - high aochildes frequency

    """
    fs = vw2fs[word]
    term1 = np.log10(fs[0] + 1)
    return term1


def find_counterbalanced_subset(first_forms: List[str],
                                min_size: int,
                                max_size: int,
                                second_forms: Optional[List[str]] = None,
                                num_tries_per_size: int = 100_000,
                                verbose: bool = False,
                                seed: int = configs.Data.seed,
                                ) -> Union[List[str], List[Tuple[str, str]]]:
    """
    find subset of first_forms from vocab words:
     - that has an acceptable number of words (between min_size and max_size), and
     - the total frequency of which is relatively equal between:
        a) aochildes
        b) wikipedia

    we use "bias" to refer to the largest word frequency difference between a) and b).

    a heuristic search is used to find such a subset.
    """

    if second_forms is not None:
        assert len(first_forms) == len(second_forms)

    np.random.seed(seed)

    if min_size <= 0:
        min_size = configs.Data.min_num_words_per_slot
    if max_size > len(first_forms):
        max_size = len(first_forms)

    # heuristic search is based on preferentially sampling words with high "rating"
    if second_forms is None:
        ratings = np.array([rate_word(w) for w in first_forms])
    else:
        ratings = np.array([rate_word(w1) * rate_word(w2) for w1, w2 in zip(first_forms, second_forms)])
    probabilities = ratings / ratings.sum()

    # helper, in case we need to counterbalance 2nd forms also
    if second_forms is None:
        first2second_form = None
    else:
        first2second_form = {w1: w2 for w1, w2 in zip(first_forms, second_forms)}

    if verbose:
        for w, p in sorted(zip(first_forms, probabilities), key=lambda i: i[1]):
            print(f'{w:<24} {p:.8f} {vw2fs[w]}')

    # try to find sample_meeting_criteria using heuristic search
    sample_meeting_criteria = None
    for subset_size in range(min_size, max_size):

        biases = []
        total_fs_list = []
        for _ in range(num_tries_per_size):
            # get a sample of words
            sample = np.random.choice(first_forms, size=subset_size, replace=False, p=probabilities).tolist()

            # compute the bias of the sample, and optionally of 2nd forms of sampled words
            total_fs = get_total_fs(sample)
            if first2second_form is not None:
                total_fs += get_total_fs([first2second_form[w] for w in sample])
            bias = calc_bias(total_fs)

            # collect bias
            biases.append(bias)
            total_fs_list.append(total_fs)

            if bias < configs.Data.bias_tolerance:
                sample_meeting_criteria = sample

        # print feedback
        idx = np.argmin(biases).item()
        feedback = f'size={subset_size:>5,}/{len(first_forms):>5,} | min bias={biases[idx]:>9,} '
        feedback += ' '.join([f'{corpus_name}={f:>9,}' for corpus_name, f in zip(column_names, total_fs_list[idx])])
        print(feedback)

        if sample_meeting_criteria:
            if first2second_form is not None:
                return [(w, first2second_form[w]) for w in sample_meeting_criteria]
            else:
                return sample_meeting_criteria

    else:
        raise RuntimeError('No word subset found that meets provided conditions')
