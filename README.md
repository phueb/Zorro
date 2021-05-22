<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

Generate test sentences and and evaluate grammatical knowledge of language models.

## About

Inspired by [BLiMP](https://arxiv.org/pdf/1912.00582.pdf),
 `Zorro` is a Python project for creating minimal pairs that exhibit a variety of grammatical contrasts,
 for analysing the grammatical knowledge of language models at various stages of training.

Sentences are created using templates, filled with words from custom, human-curated word lists. 
There are 4 phenomena, each consisting of a set of paradigms:
1. subject-verb agreement: across 0, 1, or 2 adjectives
2. demonstrative-subject agreement: across prepositional phrase, or relative clause; in 1 or 2 verb question
3. irregular verb: active voice, passive voice
4. quantifiers: existential there, superlative
5. filler-gap: wh-question object, or subject


## How words were chosen

Words that make up test sentences are all derived from a BPE encoding vocab file 
 generated using the Python `tokenizers` package. 

1. Using `script/tag_and_count_vocab_words.py`, we removed any word that is:
- not a whole word in original corpus files (it is a sub-word)
- not in th English dictionary
- a Stanford CoreNLP stop-word

2. Using `scripts/chose_legal_words.py`, we:
- automatically retrieved words tagged with desired POS
- manually tagged words as legal or illegal

## Usage

To make test sentences for a new vocabulary:

1. get vocab from which words will be chosen for inclusion in test sentences using `scripts/tag_and_count_vocab_words.py`
2. chose words to be included by part-of-speech using `scripts/chose_legal_words.py`
2. make and save test sentences using `scripts/make_sentences.py`

The grammatical correctness of each sentence is determined by its position in the text file:
- sentences on odd numbered lines (1, 3, etc.) are un-grammatical
- sentences on even numbered lines (2, 4, etc.) are grammatical


To score predictions made by your models:

1. score forced-choice predictions using `scripts/plot_accuracy.py`

