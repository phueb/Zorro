"""
present words belonging to the same POS tag for human to judge as legal or not - can they be used in test sentences?
"""
import pandas as pd

from zorro import configs
from zorro.vocab import load_vocab_df

TAG = 'VBZ'

tag2template = {
    'NN': 'look at this ADJ {}',
    'JJ': 'look at this {} NN',
    'VBD': 'sarah {} something',
    'VB': 'sarah might {} something',
    'VBG': 'sarah might be {} something',
    'VBZ': 'sarah {} something',
}


vocab_df = load_vocab_df()

nas = (configs.Dirs.external_words / "nouns_ambiguous_number.txt").open().read().split()


df_path = configs.Dirs.legal_words / f'{TAG}.csv'
if not df_path.exists():
    df_legal = pd.DataFrame(columns=['word'] + ['is_legal'])
else:
    df_legal = pd.read_csv(df_path)

# for each whole word in vocab, make new row for df
for n, (vw, vw_series) in enumerate(vocab_df.iterrows()):

    if vw in df_legal['word'].tolist():
        continue
    if vw_series['is_excluded']:
        continue

    row = {'word': vw}

    # consult spacy tag if whole word can NOT be used in this slot
    if vw_series[TAG] == 0:
        row[f'is_legal'] = 0

    elif vw in nas:
        row[f'is_legal'] = 0

    # ask user if whole word can be used in this slot
    else:
        print()
        print(tag2template[TAG].format(f'\033[94m{vw}\033[0m'))   # uses color

        is_valid = False
        while not is_valid:
            response = input('Grammatical? [f=yes j=no q=quit]')
            if response == 'f':
                row[f'is_legal'] = 1
                is_valid = True
            elif response == 'j':
                row[f'is_legal'] = 0
                is_valid = True
            elif response == 'q':
                exit('User exit')
            else:
                is_valid = False

    df_legal = df_legal.append(row, ignore_index=True)
    df_legal.to_csv(df_path, index=False)
    print(row)
    print(f'\nSaved {n}/{len(vocab_df)}\n')