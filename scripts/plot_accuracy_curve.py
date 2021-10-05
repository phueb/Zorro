"""
This script plots accuracy of model performance on Zorro test suite across training.

This script is useful for replicating results reported in Huebner et al. (2021) that introduces BabyBERTa.
Replication requires access to the shared drive (access provided to lab members only) where model results are saved.

The advantage of this script is that accuracy is plotted for each step,
making comparison more straightforward compared to using checkpoints for which information about which step they were created is not known.
Comparing models saved at different steps is not fair.



"""
from collections import defaultdict
import numpy as np
from itertools import count

from zorro.utils import prepare_data_for_plotting, get_phenomena_and_paradigms
from zorro.utils import load_group_names, filter_by_step, get_reps, get_legend_label
from zorro.io import get_group2model_output_paths
from zorro.visualizer import VisualizerLines, ParadigmDataLines

EXPERIMENT: str = 'exp1'
STEP_SIZE: int = 20_000

if EXPERIMENT == 'exp1':
    param_names = [f'param_{i:03}' for i in [1, 4]]
    conditions = ['corpora', 'leave_unmasked_prob']

elif EXPERIMENT == 'exp2':
    param_names = [f'param_{i:03}' for i in [1, 2, 3]]
    conditions = ['corpora', ]

elif EXPERIMENT == 'exp3':
    param_names = [f'param_{i:03}' for i in [5, 6]]
    conditions = ['corpora', 'load_from_checkpoint']

elif EXPERIMENT == 'exp4a':

    param_names = [f'param_{i:03}' for i in []]
    conditions = ['corpora']

elif EXPERIMENT == 'exp4b':

    param_names = [f'param_{i:03}' for i in []]
    conditions = ['leave_unmasked_prob', ]

elif EXPERIMENT == 'age-order-exp':
    param_names = [f'param_{i:03}' for i in [12, 13]]
    conditions = ['corpora', 'training_order']

else:
    raise AttributeError('Unknown experiment')

group_names = load_group_names(param_names)
labels = [get_legend_label(gn, conditions) for gn in group_names]

# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = get_phenomena_and_paradigms()

# collects and plots each ParadigmData instance in 1 multi-axis figure
v = VisualizerLines(phenomena_paradigms=phenomena_paradigms, step_size=STEP_SIZE)

# for all paradigms
for n, (phenomenon, paradigm) in enumerate(phenomena_paradigms):
    print(f'Scoring and plotting results for phenomenon={phenomenon:<36} paradigm={paradigm:<36} '
          f'{n + 1:>2}/{len(phenomena_paradigms)}')

    # load model output at all available steps
    group_name2model_output_paths = get_group2model_output_paths(group_names,
                                                                 phenomenon,
                                                                 paradigm,
                                                                 )

    # print n
    for gn, model_output_paths in group_name2model_output_paths.items():
        reps = get_reps(model_output_paths)
        print(f'{gn:.<64}n={reps:>2}')

    # init data
    group_name2rep2curve = defaultdict(dict)
    group_name2template2curve = defaultdict(dict)

    step_exists = True
    steps = []
    for step in count(0, STEP_SIZE):  # increment step until no model output is found
        print(f'step={step:>12,}')

        # filter files by step
        group2model_output_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                            for g, fps in group_name2model_output_paths.items()}

        # exit loop if no model output files available at this step
        for group, model_output_paths_at_step in group2model_output_paths_at_step.items():
            if not model_output_paths_at_step:
                step_exists = False
        if not step_exists:
            break
        else:
            steps.append(step)

        # calc + collect accuracy
        template2group_name2accuracies = prepare_data_for_plotting(group2model_output_paths_at_step,
                                                                   phenomenon,
                                                                   paradigm,
                                                                   )

        # collect average performance in each paradigm, grouped by replication - allows computation of statistics
        for group_name, accuracies in template2group_name2accuracies['all templates'].items():
            for rep, acc in enumerate(accuracies):
                group_name2rep2curve[group_name].setdefault(rep, []).append(acc)

        # collect average performance in each paradigm, grouped by template
        for template, group_name2accuracies in template2group_name2accuracies.items():
            if template == 'all templates':
                continue
            for group_name, accuracies in group_name2accuracies.items():
                curve_i = np.mean(accuracies)  # the mean proportion of a group at one location on curve
                group_name2template2curve[group_name].setdefault(template, []).append(curve_i)

    pd = ParadigmDataLines(
        steps=steps,
        phenomenon=phenomenon,
        paradigm=paradigm,
        group_names=group_names,
        labels=labels,
        group_name2rep2curve=group_name2rep2curve,
        group_name2template2curve=group_name2template2curve,
    )

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()

