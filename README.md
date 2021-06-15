<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

Generate test sentences and and evaluate grammatical knowledge of masked language models.

## About

Inspired by [BLiMP](https://arxiv.org/pdf/1912.00582.pdf),
 `Zorro` is a Python project for creating minimal pairs that exhibit a variety of grammatical contrasts,
 for analysing the grammatical knowledge of language models at various stages of training.

Sentences are created using templates, filled with words from custom, human-curated word lists. 
There are 4 phenomena, each consisting of a set of paradigms:
1. determiner-subject agreement: across prepositional phrase, or relative clause; in 1 or 2 verb question
2. subject-verb agreement: across 0, 1, or 2 adjectives
3. anaphor agreement: gender
4. argument structure: dropped arguments, swapped arguments, transitive
5. binding: principle A
6. case: subjective pronoun  (not in BLiMP)
7. ellipsis: N-bar
8. filler-gap: wh-question object, or subject
9. irregular: verb
10. island-effects: adjunct, coordinate_structure_constraint 
11. local attractor: in question with auxiliary (not in BLiMP)
12. NPI licensing: "only" licensor
13. quantifiers: existential there, superlative


## How words were chosen

Words that make up test sentences are all derived from frequent nouns, verbs and adjectives in 5M words of child-directed speech, 
5M words of child-directed written text from the Newsela corpus, and 10M words of adult-directed written text from English Wikipedia.

Note: All words were derived from whole-words in a BPE vocabulary trained using the Python `tokenizers` package on the above corpora. 

1. Using `script/tag_and_count_vocab_words.py`, we removed any word that is:
- not a whole word in original corpus files (it is a sub-word)
- not in th English dictionary
- a Stanford CoreNLP stop-word

2. Using `scripts/chose_legal_words.py`, we:
- automatically retrieved words tagged with desired POS
- manually tagged words as legal or illegal

## Usage

### To make test sentences based on a new vocabulary:

1. get vocab from which words will be chosen for inclusion in test sentences using `scripts/tag_and_count_vocab_words.py`
2. chose words to be included by part-of-speech using `scripts/chose_legal_words.py`
2. make and save test sentences using `scripts/make_sentences.py`

The grammatical correctness of each sentence is determined by its position in the text file:
- sentences on odd numbered lines (1, 3, etc.) are un-grammatical
- sentences on even numbered lines (2, 4, etc.) are grammatical


### To score predictions made by your models:

Use `scripts/plot_accuracy_single_time_point.py` or `scripts/plot_accuracy_curve.py`. 
These scripts must be pointed to text files containing sentences alongside their cross-entropy scores, 
each separated by a new line. Ordering of sentences does not matter - 
whether a sentence is grammatical or not is decided by matching the sentence to its order in the original file in `sentences/`.
 

