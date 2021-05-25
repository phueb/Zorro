from collections import defaultdict
import numpy as np
import yaml
from pathlib import Path

from zorro import configs
from zorro.prepare import prepare_data_for_plotting
from zorro.io import get_group2model_output_paths
from zorro.figs import show_barplot
from zorro.visualizer import Visualizer, ParadigmData

phenomena = [
    'npi_licensing',
    'ellipsis',
    'filler-gap',
    'case',
    'argument_structure',
    'local_attractor',
    'agreement_subject_verb',
    'agreement_demonstrative_subject',
    'irregular_verb',
    'island-effects',
    'quantifiers',
]

EXCLUDED_PARADIGMS = [
    'existential_there_2',  # too difficult
    'across_2_adjectives',  # very similar performance to across_1_adjective
]

# where to get files from?
if configs.Eval.local_runs:
    runs_path = configs.Dirs.runs_local
else:
    runs_path = configs.Dirs.runs_remote


def filter_by_step(model_output_path: Path,
                   step: int,
                   ) -> bool:
    if int(model_output_path.stem.split('_')[-1]) == step:
        return True

    return False


# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = []
for phenomenon in phenomena:
    for p in (configs.Dirs.src / phenomenon).glob('*.py'):
        paradigm = p.stem
        if paradigm in EXCLUDED_PARADIGMS:
            continue
        phenomena_paradigms.append((phenomenon, paradigm))

# collects and plots each ParadigmData instance in 1 multi-axis figure
v = Visualizer(phenomena_paradigms=phenomena_paradigms)


# for all paradigms
for phenomenon, paradigm in phenomena_paradigms:

    # group_names
    if configs.Eval.param_names is None:
        group_names_ = sorted([p.name for p in runs_path.glob('*')])
    else:
        group_names_ = configs.Eval.param_names

    # filter group_names
    if configs.Eval.included_params:
        group_names = []
        for group_name in group_names_:
            path = runs_path / group_name / 'param2val.yaml'
            with path.open('r') as f:
                param2val = yaml.load(f, Loader=yaml.FullLoader)
            for k, v in configs.Eval.included_params.items():
                if param2val[k] == v:
                    group_names.append(group_name)
    else:
        group_names = group_names_

    print(f'Found params={group_names}')

    # load model output at all available steps
    print('Loading model model output...')
    group2model_output_paths = get_group2model_output_paths(group_names,
                                                            runs_path,
                                                            phenomenon,
                                                            paradigm,
                                                            )

    # init line plot data
    pd = ParadigmData(
        phenomenon=phenomenon,
        paradigm=paradigm,
        group_name2rep2curve=defaultdict(dict),
        group_name2template2curve=defaultdict(dict),
        group_names=group_names,
        group2model_output_paths=group2model_output_paths
    )

    for step in configs.Eval.steps:
        print(f'===============\nstep={step:,}\n===============')

        # filter files by step
        group2model_output_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                            for g, fps in group2model_output_paths.items()}

        # calc + collect accuracy
        template2group_name2accuracies = prepare_data_for_plotting(group2model_output_paths_at_step,
                                                                   phenomenon,
                                                                   paradigm,
                                                                   )

        # collect average performance in each paradigm, grouped by replication - allows computation of statistics
        for group_name, accuracies in template2group_name2accuracies['all templates'].items():
            for rep, curve_i in enumerate(accuracies):
                pd.group_name2rep2curve[group_name].setdefault(rep, []).append(curve_i)

        # collect average performance in each paradigm, grouped by template
        for template, group_name2accuracies in template2group_name2accuracies.items():
            if template == 'all templates':
                continue
            for group_name, accuracies in group_name2accuracies.items():
                curve_i = np.mean(accuracies)  # the mean proportion of a group at one location on curve
                pd.group_name2template2curve[group_name].setdefault(template, []).append(curve_i)

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()

