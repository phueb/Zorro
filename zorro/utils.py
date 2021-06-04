from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from pathlib import Path
from matplotlib import rcParams
import yaml

from zorro.scoring import count_correct_choices
from zorro.data import DataExperimental
from zorro import configs

rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False


def get_reps(model_output_paths: List[Path],
             step: Union[int, None],
             ) -> int:
    if step is not None:
        pattern = f'_{step}'
    else:
        pattern = ''
    return len([path for path in model_output_paths if path.stem.endswith(pattern)])


def prepare_data_for_plotting(gn2model_output_paths: Dict[str, List[Path]],
                              phenomenon: str,
                              paradigm: str,
                              ) -> Dict[str, Dict[str, np.array]]:
    """
    :param gn2model_output_paths: dict mapping group name to paths of files containing predictions at a specific step
    :param phenomenon: name of phenomenon
    :param paradigm: name of paradigm
    :return: double-embedded dict, which can be input to barplot function

    how it works: for each group of model output:
    1. the model output are read and categorized by template (or not)
    2. scores (proportions) are stored in a matrix inside a double-embedded dict, ready for plotting

    this functions scores all model output associated with a single paradigm,
    and produces all results necessary to plot a single figure.

    'accuracies' is a vector containing accuracies, one per replication
    """

    if not configs.Eval.categorize_by_template:
        templates = ['all templates']
    else:
        raise NotImplementedError  # TODO read template info directly from local text files containing sentences

    group_names = list(gn2model_output_paths.keys())

    # init result: a vector populated with accuracies, one for each model rep, per group, per template
    res = {template: {gn: np.zeros(len(output_paths)) for gn, output_paths in gn2model_output_paths.items()}
           for template in templates}

    for group_name in group_names:

        # read model output into instance of DataExperimental
        output_paths = gn2model_output_paths[group_name]
        if not output_paths:
            print(f'Did not find model output files. Consider reducing max step. Skipping')
            continue
        data_instances = [DataExperimental(op, phenomenon, paradigm) for op in output_paths]

        for row_id, data in enumerate(data_instances):

            # organize sentence pairs by template
            if configs.Eval.categorize_by_template:
                raise NotImplementedError
            else:
                template2pairs = {templates[0]: data.pairs}

            for template in templates:

                pairs = template2pairs[template]
                assert pairs

                # calc proportion correct - sentences on odd lines are bad, and sentences on even lines are good
                num_correct = count_correct_choices(data)
                accuracy = num_correct / len(pairs)

                # populate vector of proportions - one vector per model group
                res[template][group_name][row_id] = accuracy

    return res


def get_phenomena_and_paradigms(excluded_paradigms: Optional[List[str]] = None,
                                ) -> List[Tuple[str, str]]:
    phenomena = [
        # 4
        # 'agreement_subject_verb',
        # # 2
        # 'agreement_demonstrative_subject',
        # 'filler-gap',
        # 'irregular_verb',
        # 'island-effects',
        # 'quantifiers',
        # 'npi_licensing',
        # 3
        'argument_structure',
        # 1
        # 'anaphor_agreement',
        # 'ellipsis',
        # 'binding',
        # 'case',  # not in BLiMP
        # 'local_attractor',  # not in BLiMP
    ]

    if not excluded_paradigms:
        excluded_paradigms = configs.Eval.excluded_paradigms

    # get list of (phenomenon, paradigm) tuples
    res = []
    for phenomenon in phenomena:
        phenomenon_path = (configs.Dirs.src / phenomenon)
        if not phenomenon_path.exists():
            raise OSError(f'{phenomenon_path} does not exist')
        for p in phenomenon_path.glob('*.py'):
            paradigm = p.stem
            if paradigm in excluded_paradigms:
                continue
            res.append((phenomenon, paradigm))

    return res


def filter_by_step(model_output_path: Path,
                   step: int,
                   ) -> bool:
    if int(model_output_path.stem.split('_')[-1]) == step:
        return True
    return False


def shorten_tick_labels(labels: List[Union[str,int]],
                        ) -> List[str]:
    return [str(label)[:-3] + 'K' if str(label).endswith('000') else label
            for label in labels]


def get_legend_label(group_name,
                     reps,
                     conditions: Optional[List[str]] = None,
                     add_group_name: bool = False,
                     ) -> str:

    conditions =  conditions or configs.Eval.conditions

    if group_name.endswith('frequency baseline'):
        return 'frequency baseline'

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    param2val = load_param2val(group_name, runs_path)

    if group_name.startswith('param'):
        model_name = 'BabyBERTa'
    else:
        model_name = 'RoBERTa-base'
        conditions = ['data_size']

    # init label
    res = f'{model_name} | n={reps} '

    # add corpora info
    if model_name == 'RoBERTa-base':
        if param2val['data_size'] == '10M':
            res += '| Warstadt et al., 2020 '
        elif param2val['data_size'] == '5M':
            res += '| AO-CHILDES '
        elif param2val['data_size'] == '160GB':
            res += '| Liu et al., 2019 '

    for c in conditions:
        if c == 'load_from_checkpoint' and param2val[c] != 'none':
            param2val_previous = load_param2val(param2val[c], runs_path)
            res += f'previously trained on {param2val_previous["corpora"]} '
            continue
        try:
            val = param2val[c]
        except KeyError:
            val = 'n/a'
        if isinstance(val, bool):
            val = int(val)
        res += f'| {c}={val} '

    if add_group_name:
        res += ' | ' + group_name

    # shorten and make more readable
    res = res.replace('leave_unmasked_prob_start=0.0 leave_unmasked_prob=0.0', 'no unmasking')
    res = res.replace('leave_unmasked_prob_start=0.1 leave_unmasked_prob=0.1', 'standard unmasking')
    res = res.replace('leave_unmasked_prob_start=0.0 leave_unmasked_prob=0.1', 'unmasking curriculum')

    res = res.replace("corpora=('wikipedia1', 'wikipedia2', 'wikipedia3')", 'Wiki-1 + Wiki-2 + Wiki-3')
    res = res.replace("corpora=('aochildes', 'aonewsela', 'wikipedia3')", 'AO-CHILDES + AO-Newsela + Wiki-3')

    res = res.replace("corpora=('aochildes',)", 'AO-CHILDES')
    res = res.replace("corpora=('aonewsela',)", 'AO-Newsela')
    res = res.replace("corpora=('wikipedia1',)", 'Wikipedia-1')

    res = res.replace("('aochildes',)", 'AO-CHILDES')
    res = res.replace("('aonewsela',)", 'AO-Newsela')
    res = res.replace("('wikipedia1',)", 'Wikipedia-1')

    return res


def load_param2val(group_name, runs_path):
    path = runs_path / group_name / 'param2val.yaml'
    with path.open('r') as f:
        param2val = yaml.load(f, Loader=yaml.FullLoader)
    return param2val