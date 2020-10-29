"""
make text file containing word, frequency, POS tag info
"""
import string
import spacy
import json
from pathlib import Path

from babeval import configs


with open(configs.Data.vocab_path) as f:
    w2id = json.load(f)
vocab = [w[1:] for w, i in w2id.items() if w.startswith(configs.Data.space_symbol)]

# exclude words
included = set()
nds = (configs.Dirs.external_words / "non-dictionary.txt").open().read().split()
nws = (configs.Dirs.external_words / "numbers.txt").open().read().split()
for w in vocab:
    if w in nds:
        continue
    if w in nws:
        continue
    if w.isdigit():
        continue
    if w in string.punctuation:
        continue
    included.add(w)


nlp = spacy.load('en_core_web_sm')

w2info = {}
corpus_paths = [p for p in Path(configs.Data.corpora_path).glob('*.txt')]
for c in corpus_paths:
    print(c)
for corpus_path in corpus_paths:
    with open(corpus_path) as f:
        documents = [l for l in f.readlines()]
        for n, doc in enumerate(nlp.pipe(documents, disable=['ner', 'parser'])):
            for w in doc:
                try:
                    w2info[w.text]['tags'].add(w.tag_)
                    w2info[w.text]['f'] += 1
                except KeyError:
                    w2info[w.text] = {'tags': {w.tag_}, 'f': 1}

            print(f'{corpus_path.name:<24} {n:>12,}/{len(documents):>12,}')

# save to text
num_excluded = 0
out_path = configs.Dirs.data / 'whole_words' / f'{"-".join([c.name[0] for c in corpus_paths])}.txt'
with open(out_path, 'w') as f:
    for w, info in sorted(w2info.items(), key=lambda i: i[1]['f'], reverse=True):
        if w in included:
            line = f'{w:>60} {info["f"]:>12} {" ".join(info["tags"])}'
            print(line)
            f.write(line + '\n')

            #todo keep track of no. of words from each corpus - only allow equal number to be exported