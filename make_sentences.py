from pathlib import Path

from babeval.agreement_between_neighbors.generate import main as generate_agreement_between_neighbors
from babeval.agreement_across_adjectives.generate import main as generate_agreement_across_adjectives
from babeval.agreement_across_adjectives_2.generate import main as generate_agreement_across_adjectives_2
from babeval.agreement_across_PP.generate import main as generate_agreement_across_pp
from babeval.agreement_across_RC.generate import main as generate_agreement_across_rc
from babeval.agreement_in_1_verb_question.generate import main as generate_agreement_in_1_verb_question
from babeval.agreement_in_2_verb_question.generate import main as generate_agreement_in_2_verb_question


output_folder = Path("output")

# agreement_between_neighbors
out_path = output_folder / 'agreement_between_neighbors.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_between_neighbors()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_across_adjectives
out_path = output_folder / 'agreement_across_adjectives.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_adjectives()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_across_adjectives_2
out_path = output_folder / 'agreement_across_adjectives_2.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_adjectives_2()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_across_PP
out_path = output_folder / 'agreement_across_PP.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_pp()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# agreement_across_RC
out_path = output_folder / 'agreement_across_RC.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_rc()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# generate_agreement_in_1_verb_question
out_path = output_folder / 'agreement_in_1_verb_question.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_in_1_verb_question()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

# generate_agreement_in_2_verb_question
out_path = output_folder / 'agreement_in_2_verb_question.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_in_2_verb_question()):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')