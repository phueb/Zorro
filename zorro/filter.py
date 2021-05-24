from typing import Callable, Generator

from zorro import configs


def collect_unique_pairs(gen_sentences: Callable,
                         ) -> Generator[str, None, None]:
    """
    given a generator of sentences, yield only consecutive sentence pairs if the pair was not previously collected
    """
    sentences1 = set()
    sentences2 = set()
    gen = gen_sentences()
    while len(sentences2) < configs.Data.num_pairs_per_paradigm:
        sentence1 = next(gen)
        sentence2 = next(gen)

        if sentence1 == sentence2:
            print(sentence1)
            print(sentence2)
            raise RuntimeError('Found pair of identical sentences')

        if sentence2 not in sentences2:  # check if good/grammatical sentence was not previously collected
            yield sentence1
            yield sentence2
        sentences1.add(sentence1)
        sentences2.add(sentence2)