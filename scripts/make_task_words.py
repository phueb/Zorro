"""
present word candidates in task sentences for human to judge as good or bad
"""
import importlib
import pandas as pd

from zorro import configs
from zorro.vocab import load_vocab_df

# chose one
TASK_NAMES = [
    'agreement_across_1_adjective',
    # 'agreement_across_2_adjectives',
    # 'agreement_across_PP',
    # 'agreement_across_RC',
    # 'agreement_in_1_verb_question',
    # 'agreement_in_2_verb_question',
]
WW_NAME = 'c-w-n'

vocab_df = load_vocab_df()

for task_name in TASK_NAMES:
    # load  task-relevant objects
    g = importlib.import_module(f'zorro.{task_name}.generate_forced_choice')
    df_path = configs.Dirs.task_words / f'{task_name}.csv'
    if not df_path.exists():
        task_df = pd.DataFrame(columns=['word'] + [f'{tag}-{order}' for tag, order, _ in g.rules.keys()])
    else:
        task_df = pd.read_csv(df_path)

    # for each whole word in vocab, make new row for df
    for n, (vw, vw_series) in enumerate(vocab_df.iterrows()):

        if vw in task_df['word'].tolist():
            continue
        if vw_series['is_excluded']:
            continue

        row = {'word': vw}
        for (tag, order, _), templates in g.rules.items():

            # consult spacy tag if whole word can NOT be used in this slot
            if vw_series[tag] == 0:
                row[f'{tag}-{order}'] = 0

            # ask user if whole word can be used in this slot
            else:
                print()
                for template in templates:
                    print(template.format(f'\033[94m{vw}\033[0m'))   # uses color

                is_valid = False
                while not is_valid:
                    response = input('Grammatical? [f=yes j=no q=quit]')
                    if response == 'f':
                        row[f'{tag}-{order}'] = 1
                        is_valid = True
                    elif response == 'j':
                        row[f'{tag}-{order}'] = 0
                        is_valid = True
                    elif response == 'q':
                        exit('User exit')
                    else:
                        is_valid = False

        task_df = task_df.append(row, ignore_index=True)
        task_df.to_csv(df_path, index=False)
        print(row)
        print(f'\nSaved {n}/{len(vocab_df)}\n')