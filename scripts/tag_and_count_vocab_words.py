"""
make csv file containing information about all words in a vocab file
"""
import spacy
import json
from pathlib import Path
import pandas as pd

from zorro import configs


with open(configs.Data.vocab_path) as f:
    w2id = json.load(f)
vocab = {w.strip(configs.Data.space_symbol) for w in w2id.keys()}

# keep track of which words are excluded - not a candidate for being inserted into test sentences
nds = (configs.Dirs.external_words / "non-dictionary.txt").open().read().split()
nws = (configs.Dirs.external_words / "numbers.txt").open().read().split()
sws = (configs.Dirs.external_words / "stopwords.txt").open().read().split()
excluded_words = set(nds + nws + sws)


def is_excluded(w: str):
    """excluded from being considered as candidate for insertion into test sentences"""
    if w in excluded_words:
        return True
    if w.isdigit():
        return True
    if len(w) == 1:
        return True
    if w.startswith(configs.Data.space_symbol):
        return True
    return False


def init_row(word: str,
             tag: str,
             corpus_abbreviation_: str,
             is_excluded_: bool = False,
             ):
    res = {
        'NN': 1 if tag == 'NN' else 0,
        'NNS': 1 if tag == 'NNS' else 0,
        'JJ': 1 if tag == 'JJ' else 0,
        'total-frequency': 1 if not is_excluded_ else 0,
        'is_excluded': is_excluded_ or is_excluded(word),
    }
    for ca in corpus_abbreviations:
        res[f'{ca}-frequency'] = 1 if ca == corpus_abbreviation_ else 0

    return res


nlp = spacy.load('en_core_web_sm')

corpus_paths = [p for p in Path(configs.Data.corpora_path).glob('*.txt')]
for c in corpus_paths:
    print(c)

# get information about all words in corpora
w2row = {}
corpus_abbreviations = [c.name[0] for c in corpus_paths]
for corpus_path, corpus_abbreviation in zip(corpus_paths, corpus_abbreviations):
    with open(corpus_path) as f:
        documents = [l for l in f.readlines()]  #[:100]  # todo
        for n, doc in enumerate(nlp.pipe(documents, disable=['ner', 'parser'])):
            for sw in doc:
                try:
                    w2row[sw.text]['NN'] += 1 if sw.tag_ == 'NN' else 0
                    w2row[sw.text]['NNS'] += 1 if sw.tag_ == 'NNS' else 0
                    w2row[sw.text]['JJ'] += 1 if sw.tag_ == 'JJ' else 0
                    w2row[sw.text]['total-frequency'] += 1
                    w2row[sw.text][f'{corpus_abbreviation}-frequency'] += 1
                except KeyError:
                    w2row[sw.text] = init_row(sw.text, sw.tag_, corpus_abbreviation)

            print(f'{corpus_path.name:<24} {n:>12,}/{len(documents):>12,}')


# ensure each word in df is a word in vocab (including sub-words)
rows = []
words = []
for w in vocab:
    if w not in w2row:
        print(w)
        w2row[w] = init_row(w, 'n/a', 'n/a', is_excluded_=True)
    rows.append(w2row[w])
    words.append(w)

# make data frame that holds info about each word in vocabZ
df = pd.DataFrame(data=rows, index=words)
df.sort_values(by='total-frequency', inplace=True, ascending=False)
print(df.head(10))

# save to csv
num_excluded = 0
out_path = configs.Dirs.data / 'vocab_words' / f'{"-".join(corpus_abbreviations)}.csv'
df.to_csv(out_path, index=True)
