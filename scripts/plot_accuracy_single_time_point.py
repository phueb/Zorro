"""
compare accuracy between models saved in local or remote runs folder, at one time step.
"""
from collections import defaultdict
from typing import List
import numpy as np

from zorro import configs
from zorro.visualizer import VisualizerBars, ParadigmDataBars
from zorro.utils import prepare_data_for_plotting, get_phenomena_and_paradigms
from zorro.io import get_group2model_output_paths


STEP = '*'
LOCAL = True
GROUP_NAMES: List[str] = []
configs.Eval.conditions = ['leave_unmasked_prob']


# get files locally, where we have runs at single time points only
if LOCAL:
    runs_path = configs.Dirs.runs_local
    configs.Eval.local_runs = True
else:
    runs_path = configs.Dirs.runs_remote
    configs.Eval.local_runs = False

group_names = sorted([p.name for p in runs_path.glob('*')])
if GROUP_NAMES:
    group_names = [gn for gn in group_names if gn in GROUP_NAMES]

if not group_names:
    raise RuntimeError(f'Did not find model output files for {GROUP_NAMES}.'
                       f' Check configs.Eval.param_names')
else:
    print(f'Found {group_names}')

# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = get_phenomena_and_paradigms()

# collects and plots each ParadigmData instance in 1 multi-axis figure
v = VisualizerBars(phenomena_paradigms=phenomena_paradigms)

# for all paradigms
for n, (phenomenon, paradigm) in enumerate(phenomena_paradigms):
    print(f'Scoring and plotting results for phenomenon={phenomenon:<36} paradigm={paradigm:<36} '
          f'{n + 1:>2}/{len(phenomena_paradigms)}')

    # load model output at all available steps
    group_name2model_output_paths = get_group2model_output_paths(group_names,
                                                                 runs_path,
                                                                 phenomenon,
                                                                 paradigm,
                                                                 step=STEP,
                                                                 )

    # init data
    group_name2template2acc = defaultdict(dict)
    group_name2rep2acc = defaultdict(dict)

    # calc + collect accuracy
    template2group_name2accuracies = prepare_data_for_plotting(group_name2model_output_paths,
                                                               phenomenon,
                                                               paradigm,
                                                               )

    # collect average performance in each paradigm, grouped by replication - allows computation of statistics
    for group_name, accuracies in template2group_name2accuracies['all templates'].items():
        for rep, acc in enumerate(accuracies):
            group_name2rep2acc[group_name][rep] = acc  # collapsed over templates

    # collect average performance in each paradigm, grouped by template
    for template, group_name2accuracies in template2group_name2accuracies.items():
        if template == 'all templates':
            continue
        for group_name, accuracies in group_name2accuracies.items():
            acc_avg_over_reps = np.mean(accuracies)  # average over reps
            group_name2template2acc[group_name][template] = acc_avg_over_reps

    pd = ParadigmDataBars(
        phenomenon=phenomenon,
        paradigm=paradigm,
        group_name2model_output_paths=group_name2model_output_paths,
        group_name2template2acc=group_name2template2acc,
        group_name2rep2acc=group_name2rep2acc,
    )

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()
