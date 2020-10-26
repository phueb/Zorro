# Babeval
Generate test sentences for evaluating NLP system trained on masked language modeling objective

## Test sentences

Sentences are created using templates, filled with custom, human-curated word lists.


## Organization

Each grammatical task (e.g. number agreement across relative clause) is associated with a folder in `babeval`.
There are two flavors of each task:
1. open-ended: model to be evaluated, predicts whatever word, in its vocabulary, replaces [MASK] best.
2. forced-choice: model to be evaluated, must chose between two alternative sentences.

Each task flavor is associated with 2 files, one for generating, and another for scoring predictions.

## How words were chosen

Words that make up test sentences are all derived from whole words in a BPE encoding vocab file:

1. Removed words
- not in original corpus files (e.g. sub-words)
- not in English dictionary
- not title-cased

2. removed  the following kinds of words manually:
- gerunds
- quantifiers: lots, some, many, none, plenty, anything, something, anyone, someone, somehow, everybody, everyone, nobody, some, sort, whoever
- number, day, and month words
- greetings: hey, hi, goodbye, hello ...
- interjections: hurrah, hurray, jeez, darn, nope, okay, oh, oops, ow, pardon, phooey, please, aha, psst, sh, shoo, sorry, uh, um, wee, whew, whoa, whoops, whoosh, wow, yuck, yucky, yum, yummy, yo, yep, yeah, achoo, goodness, hurrah, peekaboo, phooey
- onomatopoeia: oink, kaboom, meow, plop, ...
- locations: downstairs, outdoors, someplace, somewhere, wherever
- times: today, tonight, tomorrow, yesterday, sometime, everyday, whenever

3. for every slot in every task, a unique word list was created in the following manner:
- start with word list from 2.
- remove any words not tagged by NLTK as belonging to a desired part-of-speech
- lastly, human annotators removed words that were judged to be ungrammatical -
e.g. for the task `agreement_across_adjectives`, annotators were given the instruction: 
"Does the word fit the slot in `Look at these _ ?`"