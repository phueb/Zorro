from pathlib import Path

from babeval.agreement_across_adjectives.generate import main as generate_agreement_across_adjectives
from babeval.agreement_across_PP.generate import main as generate_agreement_across_pp
from babeval.agreement_across_RC.generate import main as generate_agreement_across_rc
from babeval.agreement_in_question.generate import main as generate_agreement_in_question

VOCAB_SIZE = 4096  # TODO verify that word lists contents are in vocab

data_folder = Path("word_lists")
output_folder = Path("output")

# open and read word_lists
with open(data_folder / "nouns.txt") as f:
    nouns = f.read().split("\n")
with open(data_folder / "adjectives.txt") as f:
    adjectives = f.read().split("\n")
with open(data_folder / "prepositions.txt") as f:
    prepositions_list = f.read().split("\n")
with open(data_folder / "pronouns.txt") as f:
    pronouns = f.read().split("\n")
with open(data_folder / "pronouns_third_person.txt") as f:
    pronouns_3p = f.read().split("\n")

# agreement_across_adjectives
out_path = output_folder / 'agreement_across_adjectives.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_adjectives(adjectives)):
        f.write(sentence + '\n')
    print(f'Saved {n:,} sentences to {out_path}')

raise SystemExit('User exit')

# agreement_across_PP
out_path = output_folder / 'agreement_across_PP.txt'
with open(out_path, 'w') as f:
    for n, sentence in enumerate(generate_agreement_across_pp(prepositions_list, nouns, adjectives)):
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


# To randomly select test_sentences to print out:

# with open(file_name) as f:
# 	f_lst = f.read().split("\n")

# rng = default_rng()
# numbers = rng.choice(len(f_lst), size=2500, replace=False)

# for i in numbers:
# 	print(f_lst[i], file = open("file_name","a"))
