

categories = ['adjectives']
included = {4096: {'annotator1': {c: None for c in categories},
                   'annotator2': {c: None for c in categories}}
            }


included[4096]['annotator1']['adjectives'] = open('word_lists/4096/adjectives_annotator1.txt', 'r').read().split()
included[4096]['annotator2']['adjectives'] = open('word_lists/4096/adjectives_annotator2.txt', 'r').read().split()


def categorize(vocab, vocab_size):

    result = {}

    for category in categories:
        result[category] = [w for w in vocab if w in
                            included[vocab_size]['annotator1'][category] +
                            included[vocab_size]['annotator2'][category]
                            ]

    return result

