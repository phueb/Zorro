from pathlib import Path

from babeval.agreement_across_adjectives.generate import main as generate_agreement_across_adjectives
from babeval.agreement_across_PP.generate import main as generate_agreement_across_pp
from babeval.agreement_across_RC.generate import main as generate_agreement_across_rc
from babeval.agreement_in_question.generate import main as generate_agreement_in_question

from babeval.vocab import get_vocab
from babeval.manual_categories import categorize

VOCAB_NAME = "childes-20191206_vocab.txt"
VOCAB_SIZE = 4096

output_folder = Path("output")

vocab_dict = categorize(get_vocab(VOCAB_NAME, VOCAB_SIZE), VOCAB_SIZE)
adjectives = vocab_dict['adjectives']

# TODO
# nouns = vocab_dict['adjectives']
# prepositions = vocab_dict['adjectives']
# pronouns = vocab_dict['pronouns']
# pronouns_3p = vocab_dict['pronouns_3p']

# agreement_across_adjectives
out_path = output_folder / 'agreement_across_adjectives.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_adjectives(adjectives)):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

raise SystemExit('Just working on above task for now.')

# agreement_across_PP
out_path = output_folder / 'agreement_across_PP.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_pp(prepositions, nouns, adjectives)):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_across_RC
out_path = output_folder / 'agreement_across_RC.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_rc(nouns, pronouns, adjectives, pronouns_3p)):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_in_question
out_path = output_folder / 'agreement_in_question.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_in_question(nouns)):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')