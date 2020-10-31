<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

Generate test sentences for evaluating NLP system trained on masked language modeling objective

## Test sentences

Sentences are created using templates, filled with words from custom, human-curated word lists.


## Organization

Each grammatical task (e.g. number agreement across relative clause) is associated with a folder in `babeval`.
There are two flavors of each task:
1. open-ended: model to be evaluated, predicts whatever word, in its vocabulary, replaces `<MASK>` best.
2. forced-choice: model to be evaluated, must chose between two alternative sentences.

Each task flavor is associated with 2 files, one for generating, and another for scoring predictions.

## How words were chosen

Words that make up test sentences are all derived from a BPE encoding vocab file 
 generated using the Python `tokenizers` package. 


1. Using `script/tag_and_count_whole_words.py`, we removed any words:
- not in original corpus files (e.g. sub-words)
- not in English dictionary
- is a number
- is a Stanford CoreNLP stopword

2. Using `scripts/make_task_words.py`, for every slot in every task, we:
- automatically retrieved words tagged with desired POS
- manually removed words that were judged to be ungrammatical:
e.g. for the task `agreement_across_adjectives`, annotators were given the instruction: 
"Does the word fit the slot in `Look at these _ ?`"
