"""
present word candidates in task sentences for human to judge as good or bad
"""
import importlib
import pandas as pd

from babeval import configs
from babeval.whole_words import get_ww2info

# chose one
TASK_NAMES = [
    # 'agreement_across_1_adjective',
    # 'agreement_across_2_adjectives',
    'agreement_across_PP',
    # 'agreement_across_RC',
    # 'agreement_in_1_verb_question',
    # 'agreement_in_2_verb_question',
]
WW_NAME = 'c-w-n'

ww2info = get_ww2info()

for task_name in TASK_NAMES:
    # load  task-relevant objects
    g = importlib.import_module(f'babeval.{task_name}.generate_forced_choice')
    df_path = configs.Dirs.task_words / f'{task_name}.csv'
    if not df_path.exists():
        df = pd.DataFrame(columns=['word'] + [f'{tag}-{order}' for tag, order, _ in g.rules.keys()])
    else:
        df = pd.read_csv(df_path)

    # for each whole word, make new row for df
    for ww, info in ww2info.items():
        if ww in df['word'].tolist():
            continue

        row = {'word': ww}
        for (tag, order, _), templates in g.rules.items():

            # ask spacy tag if whole word can NOT be used in this slot
            if tag not in info[1]:
                row[f'{tag}-{order}'] = 0

            # ask user if whole word can be used in this slot
            else:
                print()
                for template in templates:
                    print(template.format(f'\033[94m{ww}\033[0m'))   # uses color

                is_valid = False
                while not is_valid:
                    response = input('Grammatical? [g(rammatical))/n(o)/q(uit)]')
                    if response == 'g':
                        row[f'{tag}-{order}'] = 1
                        is_valid = True
                    elif response == 'n':
                        row[f'{tag}-{order}'] = 0
                        is_valid = True
                    elif response == 'q':
                        exit('User exit')
                    else:
                        is_valid = False

        df = df.append(row, ignore_index=True)
        df.to_csv(df_path, index=False)
        print(row)
        print('\nSaved\n')