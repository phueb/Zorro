
## How are words for test sentences chosen?

### Chose a vocab size
The starting point for all words is the set of 4K most frequent words in a 5M word corpus of child-directed speech, called childes-20191206.


### Start with auto-tagging
Each word in the 4K vocab is POS-tagged using the Python library NLTK.
All NLTK generated files are found in this directory, called `nltk_results`. 

### Use human annotators
Each task has a template, and human annotators decide whether a word can be used to fill a slot in the template.
For example, if a template contains a noun slot, a human annotator is given a list of nouns found by NLTK to decide, for each noun, whether it can be used to fill the noun slot.
Files with `annotator1` or `annotator2` in the name contain words tagged manually by human annotators, and are stored separately for each task.



