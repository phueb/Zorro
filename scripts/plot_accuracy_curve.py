from collections import defaultdict
import numpy as np
import yaml

from zorro import configs
from zorro.utils import prepare_data_for_plotting, get_phenomena_and_paradigms, filter_by_step
from zorro.io import get_group2model_output_paths
from zorro.visualizer import VisualizerLines, ParadigmDataLines


# where to get files from?
if configs.Eval.local_runs:
    runs_path = configs.Dirs.runs_local
else:
    runs_path = configs.Dirs.runs_remote

# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = get_phenomena_and_paradigms()

# collects and plots each ParadigmData instance in 1 multi-axis figure
v = VisualizerLines(phenomena_paradigms=phenomena_paradigms)


# for all paradigms
for n, (phenomenon, paradigm) in enumerate(phenomena_paradigms):
    print(f'Scoring and plotting results for phenomenon={phenomenon:<36} paradigm={paradigm:<36} '
          f'{n + 1:>2}/{len(phenomena_paradigms)}')

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
    group_name2model_output_paths = get_group2model_output_paths(group_names,
                                                                 runs_path,
                                                                 phenomenon,
                                                                 paradigm,
                                                                 )

    group_name2rep2curve = defaultdict(dict)
    group_name2template2curve = defaultdict(dict)

    for step in configs.Eval.steps:
        print(f'step={step:>12,}')

        # filter files by step
        group2model_output_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                            for g, fps in group_name2model_output_paths.items()}

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
        phenomenon=phenomenon,
        paradigm=paradigm,
        group_name2rep2curve=group_name2rep2curve,
        group_name2template2curve=group_name2template2curve,
        group_name2model_output_paths=group_name2model_output_paths,
    )

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()

