import random
from typing import List, Dict, Tuple
import inflect

from zorro.vocab import get_vocab_words
from zorro.counterbalance import find_counterbalanced_subset
from zorro import configs

NUM_ADJECTIVES = 50
NUM_NOUNS = 50

template = '{} {} {} {} .'

templates = []  # TODO define templates once everywhere

plural = inflect.engine()


def main():
    """
    example:
    "a big dog fell down the stairs ." vs. "a big dog fallen down the stairs ."

    """

    names_ = [
        'michael',
        'simon',
        'allen',
        'obama',
        'donald',
        'henry',
        'robert',
        'bill',
        'thomas',
        'mark',
        'richard',
        'louis',
        'joseph',
        'edward',
        'sarah',
        'laura',
        'allen',
        'maria',
        'ben',
        'gregory',
        'taylor',
        'chris',
        'carter',
        'sam',
        'roger',
        'anne',
    ]

    vocab = get_vocab_words()
    modifiers = ['over there', 'some time ago', 'this morning', 'at home', 'last night']

    names = find_counterbalanced_subset(names_, min_size=10, max_size=len(names_))

    vbds_vbns_args = [
        ('arose', 'arisen', ['']),

        # optional arguments
        ('knew', 'known', ['a lot of things', 'she could do it']),
        ('saw', 'seen', ['a bird', 'a shape', 'something']),
        ('began', 'begun', ['to work']),
        ('fell', 'fallen', ['down the stairs']),
        ('flew', 'flown', ['into the sky', 'away']),
        ('drove', 'driven', ['out of the garage', 'down the road', 'with one wheel', 'without looking']),
        ('grew', 'grown', ['quickly',]),
        ('hid', 'hidden', ['from view', 'behind the bush']),
        ('rose', 'risen', ['from bed']),
        ('swore', 'sworn', ['not to do it again']),
        ('drank', 'drunk', ['some juice', 'the soup', 'your coffee']),
        ('ate', 'eaten', ['a lot', 'more than me', 'some ice cream']),
        ('drew', 'drawn', ['a picture', 'a map', 'a round circle']),
        ('wrote', 'written', ['a story', 'a note', 'into a book', 'with a large pen']),
        ('sang', 'sung', ['a nice song', 'in the theater', 'with a pretty voice', 'my favorite song']),
        ('spoke', 'spoken', ['very loudly', 'to me', 'about many things', 'without thinking']),
        ('came', 'come', ['to the store', 'just in time', 'when we needed her', 'too late']),

        # transitive
        ('was', 'been', ['here', 'alone', 'afraid']),
        ('beat', 'beaten', ['the dough', 'a little boy', 'their pet']),
        ('became', 'become', ['angry', 'very different', 'someone else']),
        ('bit', 'bitten', ['her own tongue', 'into the cake', 'off a big chunk']),
        ('blew', 'blown', ['out the candle', 'away the dirt',]),
        ('chose', 'chosen', ['the best option', 'the cheaper item', ]),
        ('did', 'done', ['nothing wrong', 'something bad', 'the best she could ']),
        ('forgave', 'forgiven', ['her', 'the child', 'him']),
        ('gave', 'given', ['a book to a student', 'a cracker to the baby', 'a coin to the stranger']),
        ('rode', 'ridden', ['a horse', 'a cart', 'in the front seat', 'away']),
        ('shook', 'shaken', ['the plate', 'the table', 'the bowl']),
        ('strode', 'stridden', ['']),
        ('took', 'taken', ['the paper', 'the garbage', 'the bell']),
        ('threw', 'thrown', ['the trash out', 'the paper ball', 'the coin', 'his ball']),
    ]

    def gen_sentences():
        while True:

            # random choices
            name = random.choice(names)
            mod = random.choice(modifiers)
            vbd, vbn, args = random.choice(vbds_vbns_args)
            arg = random.choice(args)

            if (vbd not in vocab or vbn not in vocab) or vbd == vbn:
                # print(f'"{verb_base:<22} excluded due to some forms not in vocab')
                continue
            if arg == '':
                continue

            # vbd is correct
            yield template.format(name, vbn, arg, mod)  # bad
            yield template.format(name, vbd, arg, mod)  # good

            # vbn is correct
            yield template.format(name, 'had ' + vbd, arg, mod)
            yield template.format(name, 'had ' + vbn, arg, mod)

    # only collect unique sentences
    sentences = set()
    gen = gen_sentences()
    while len(sentences) // 2 < configs.Data.num_pairs_per_paradigm:
        sentence = next(gen)
        if sentence not in sentences:
            yield sentence
        sentences.add(sentence)


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[-1] == '.':
            template2pairs.setdefault(templates[0], []).append(pair)

        else:
            raise ValueError(f'Failed to categorize {pair} to template.')

    return template2pairs


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n//2+1:>12,}', s)
