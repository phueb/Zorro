from collections import defaultdict
import numpy as np
import yaml
from pathlib import Path
from itertools import product, chain

from zorro import configs
from zorro.prepare import prepare_data_for_plotting
from zorro.io import get_group2predictions_file_paths
from zorro.figs import show_barplot
from zorro.visualizer import Visualizer, ParadigmData

SHOW_BAR_PLOTS = False

phenomena = [
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

SKIP_PARADIGMS = [
    'existential_there_2'  # too difficult
    'across_2_adjectives'  # very similar performance to across_1_adjective
]

# where to get files from?
if configs.Eval.local_runs:
    runs_path = configs.Dirs.runs_local
else:
    runs_path = configs.Dirs.runs_remote


def filter_by_step(prediction_file_path: Path,
                   step: int,
                   ) -> bool:
    if int(prediction_file_path.stem.split('_')[-1]) == step:
        return True

    return False


# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = list(chain(*[product([phenomenon],
                                           [p.stem for p in (configs.Dirs.src / phenomenon).glob('*.py')])
                                   for phenomenon in phenomena]))

# collects and plots each ParadigmData instance in 1 multi-axis figure
v = Visualizer(num_paradigms=len(phenomena_paradigms) - len(SKIP_PARADIGMS),
               y_lims=[0.5, 1.01])


def shorten(name: str):
    """make name of phenomenon shorter to fit in figure"""
    name = name.replace('demonstrative', 'det.')
    return name


# for all paradigms
for phenomenon, paradigm in phenomena_paradigms:
    if paradigm in SKIP_PARADIGMS:
        continue

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

    # load prediction files at all available steps
    print('Loading model prediction files...')
    group2predictions_file_paths = get_group2predictions_file_paths(group_names,
                                                                    runs_path,
                                                                    phenomenon,
                                                                    paradigm,
                                                                    )

    # init line plot data
    pd = ParadigmData(
        name=f'{shorten(phenomenon)}\n{paradigm}',
        group_name2rep2curve=defaultdict(dict),
        group_name2template2curve=defaultdict(dict),
        group_names=group_names + configs.Data.control_names,
        group2prediction_file_paths=group2predictions_file_paths
    )

    for step in configs.Eval.steps:
        print(f'===============\nstep={step:,}\n===============')

        # filter files by step
        group2predictions_file_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                                for g, fps in group2predictions_file_paths.items()}

        # calc + collect accuracy
        template2group_name2props = prepare_data_for_plotting(group2predictions_file_paths_at_step,
                                                              phenomenon,
                                                              paradigm,
                                                              )

        # plot accuracy comparison at current time step
        if SHOW_BAR_PLOTS:
            show_barplot(template2group_name2props,
                         group2predictions_file_paths,
                         paradigm,
                         step,
                         verbose=True,
                         )

        # collect average performance in each paradigm, grouped by replication - allows computation of statistics
        for group_name, props in template2group_name2props['all templates'].items():
            for rep, curve_i in enumerate(props):
                pd.group_name2rep2curve[group_name].setdefault(rep, []).append(curve_i)

        # collect average performance in each paradigm, grouped by template
        for template, group_name2props in template2group_name2props.items():
            if template == 'all templates':
                continue
            for group_name, props in group_name2props.items():
                curve_i = np.mean(props)  # the mean proportion of a group at one location on curve
                pd.group_name2template2curve[group_name].setdefault(template, []).append(curve_i)

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()
v.plot_with_legend()
