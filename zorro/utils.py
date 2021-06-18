from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
from pathlib import Path
from matplotlib import rcParams
import yaml

from zorro.scoring import count_correct_choices
from zorro.data import DataExperimental

from zorro import configs

rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False

names_ = (configs.Dirs.legal_words / 'names.txt').open().read().split()


def capitalize_names_in_sentence(s: str):
    """
    case-sensitive models require upper-cased names otherwise they are split into sub-tokens,
    and thus artificially deflates accuracy on grammar test suite
    """
    for name in names_:
        if name in s:
            s = s.replace(name + ' ', name.capitalize() + ' ')
    return s


def get_reps(model_output_paths: List[Path],
             ) -> int:
    file_names = [p.name for p in model_output_paths]
    return len(model_output_paths) // len(set(file_names))


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
                try:
                    num_correct = count_correct_choices(data)
                except KeyError:  # can occur when model was evaluated on a different version of the test suite
                    raise RuntimeError(f'The model {group_name} was evaluated on a pair that is not in test suite.')
                accuracy = num_correct / len(pairs)

                # populate vector of proportions - one vector per model group
                res[template][group_name][row_id] = accuracy

    return res


def get_phenomena_and_paradigms(excluded_paradigms: Optional[List[str]] = None,
                                ) -> List[Tuple[str, str]]:
    phenomena = [
        # 4
        'agreement_subject_verb',
        # 2
        'agreement_determiner_noun',
        'filler-gap',
        'island-effects',
        'quantifiers',
        'npi_licensing',
        # 3
        'argument_structure',
        # 1
        'irregular',
        'anaphor_agreement',
        'ellipsis',
        'binding',
        'case',  # not in BLiMP
        'local_attractor',  # not in BLiMP
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
            if paradigm not in excluded_paradigms:
                res.append((phenomenon, paradigm))

    return res


def filter_by_step(model_output_path: Path,
                   step: int,
                   ) -> bool:
    if int(model_output_path.stem.split('_')[-1]) == step:
        return True
    return False


def shorten_tick_label(label: Union[str, int],
                       ) -> str:
    if str(label).endswith('000'):
        return str(label)[:-3] + 'K'
    else:
        return label


def get_legend_label(group_name,
                     conditions: Optional[List[str]] = None,
                     add_data_size: bool = False,
                     add_group_name: bool = False,
                     ) -> str:

    conditions = conditions or []

    if 'data_size' not in conditions and add_data_size:
        conditions.insert(0, 'data_size')

    if group_name.endswith('frequency baseline'):
        return 'frequency baseline'

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    param2val = load_param2val(group_name, runs_path)

    if 'BabyBERTa' in group_name or 'param_' in group_name:
        model_name = 'BabyBERTa'
    elif 'RoBERTa-base' in group_name or 'Roberta-base' in group_name:
        model_name = 'RoBERTa-base'
    else:
        raise AttributeError(f'Did not recognize {group_name}. BabyBERTa or RoBERTa-base?')

    # init label
    res = f'{model_name} '

    for c in conditions:
        if c == 'load_from_checkpoint' and param2val[c] != 'none':
            try:
                param2val_previous = load_param2val(param2val[c], runs_path.parent / 'runs_saved')
            except FileNotFoundError:
                res += f'| loaded from {param2val[c]} '
            else:
                res += f'| previously trained on {param2val_previous["corpora"]} '
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
    res = res.replace('leave_unmasked_prob_start=0.0 | leave_unmasked_prob=0.0', 'no unmasking')
    res = res.replace('leave_unmasked_prob_start=0.1 | leave_unmasked_prob=0.1', 'standard unmasking')
    res = res.replace('leave_unmasked_prob_start=0.0 | leave_unmasked_prob=0.1', 'unmasking curriculum')

    res = res.replace('leave_unmasked_prob=0.0', 'no unmasking')
    res = res.replace('leave_unmasked_prob=n/a', 'standard unmasking')
    res = res.replace('leave_unmasked_prob=0.1', 'standard unmasking')

    res = res.replace("corpora=('wikipedia1', 'wikipedia2', 'wikipedia3')", 'Wiki-1 + Wiki-2 + Wiki-3')
    res = res.replace("corpora=('aochildes', 'aonewsela', 'wikipedia3')", 'AO-CHILDES + AO-Newsela + Wiki-3')

    res = res.replace("('aochildes',)", 'AO-CHILDES')
    res = res.replace("('aonewsela',)", 'AO-Newsela')
    res = res.replace("('wikipedia1',)", 'Wikipedia-1')

    res = res.replace("data_size=", '')
    res = res.replace("corpora=", '')

    return res


def load_param2val(group_name, runs_path):
    path = runs_path / group_name / 'param2val.yaml'
    with path.open('r') as f:
        param2val = yaml.load(f, Loader=yaml.FullLoader)
    return param2val


def load_group_names(param_names: Optional[List[str]] = None,
                     included_params: Dict[str, Any] = None,
                     ) -> List[str]:

    # get files locally, where we have runs at single time points only
    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    if param_names is None:
        group_names_ = sorted([p.name for p in runs_path.glob('*')])
    else:
        group_names_ = param_names

    # filter
    if included_params:
        res = []
        for gn in group_names_:
            path = runs_path / gn / 'param2val.yaml'
            with path.open('r') as f:
                param2val = yaml.load(f, Loader=yaml.FullLoader)
            for k, v in included_params.items():
                if param2val[k] == v:
                    res.append(gn)
    else:
        res = group_names_

    if not res:
        raise RuntimeError(f'Did not find model output files for {res}.'
                           f' Check configs.Eval.param_names')
    else:
        print(f'Found {res}')

    return res
