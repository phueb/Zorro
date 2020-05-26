import random

template = '{} {} [MASK] .'

start_words = ['this', 'these', 'that', 'those']


def main(adjectives_list):
    """
    number of sentences = # start-words * # adjectives * 3
    """
    for start_word in start_words:

        al1 = random.sample(adjectives_list, k=len(adjectives_list))
        al2 = random.sample(adjectives_list, k=len(adjectives_list))
        al3 = random.sample(adjectives_list, k=len(adjectives_list))

        for adj1, adj2, adj3 in zip(al1, al2, al3):
            yield template.format(start_word, ' '.join([adj1]))
            yield template.format(start_word, ' '.join([adj1, adj2]))
            yield template.format(start_word, ' '.join([adj1, adj2, adj3]))