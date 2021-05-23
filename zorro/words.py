from typing import List, Optional, Tuple, Union
import pandas as pd
import functools
import inflect
from lemminflect import getInflection, getLemma

from zorro import configs
from zorro.counterbalance import find_counterbalanced_subset
from zorro.vocab import get_vocab_words


vocab = get_vocab_words()


@functools.lru_cache(maxsize=12)
def get_legal_words(tag: str,
                    second_tag: Optional[str] = None,  # also counterbalance list of other word forms (e.g. plural)
                    seed: int = configs.Data.seed,
                    exclude: Optional[Tuple[str, ...]] = None,
                    verbose: bool = False,
                    ) -> Union[List[str], List[Tuple[str, str]]]:

    print(f'Obtaining counterbalanced subset of legal words with tag={tag} and second_tag={second_tag}')

    # get words with requested tag and order
    df_legal = pd.read_csv(configs.Dirs.legal_words / f'{tag}.csv')
    bool_ids = df_legal['is_legal'].astype(bool).tolist()
    first_forms_ = df_legal['word'][bool_ids].tolist()

    # exclude any words ?
    if exclude:
        first_forms_ = [w for w in first_forms_ if w not in exclude]

    # also counterbalance 2nd forms of words ?
    if second_tag is None:
        second_forms_ = None
    elif second_tag == 'NNP':
        plural = inflect.engine()
        second_forms_ = [plural.plural(w) for w in first_forms_]
    elif second_tag.startswith('VB'):
        lemmas = [getLemma(w, upos='VERB')[0] for w in first_forms_]
        second_forms_ = [getInflection(lemma, tag=second_tag)[0] for lemma in lemmas]  # requires lemma as input
    else:
        raise AttributeError('Invalid arg to second_tag')

    # remove words if their 2nd form is not in vocab or if it is identical to 1st form
    if second_tag is not None:
        first_forms = []
        second_forms = []
        for w1, w2 in zip(first_forms_, second_forms_):
            if w2 in vocab and w2 != w1:
                first_forms.append(w1)
                second_forms.append(w2)
                if verbose:
                    print(f'Included {w1:<12} and {w2:<12}')
        assert first_forms
        assert second_forms
    else:
        first_forms = first_forms_
        second_forms = second_forms_

    # find subset of words such that their total corpus frequencies are approx equal across corpora
    num_words_in_sample = configs.Data.tag2num_words[tag]
    res = find_counterbalanced_subset(first_forms,
                                      min_size=num_words_in_sample,
                                      max_size=num_words_in_sample+100,
                                      second_forms=second_forms,
                                      seed=seed,
                                      verbose=verbose,
                                      )

    return res
