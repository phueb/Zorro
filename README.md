# Babeval
Generate test sentences for evaluating NLP system trained on masked language modeling objective

## Test sentences

Sentences are created using templates, filled with words from the 4K most frequent words in a custom version of
the American-English CHILDES corpus. 


## Organization

Each grammatical task (e.g. number agreement across relative clause) is associated with a folder in `babeval`.
There are two flavors of each task:
1. open-ended: model to be evaluated, predicts whatever word, in its vocabulary, replaces [MASK] best.
2. forced-choice: model to be evaluated, must chose between two alternative sentences.

Each task flavor is associated with 2 files, one for generating, and another for scoring predictions

