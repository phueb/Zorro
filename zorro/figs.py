import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import yaml
from pathlib import Path
from matplotlib import rcParams

from zorro import configs

rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False


def get_legend_label(group2predictions_file_paths,
                     param_name,
                     show_step: bool = True,
                     ) -> str:
    if 'baseline' in param_name:
        return param_name

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    path = runs_path / param_name / 'param2val.yaml'
    with path.open('r') as f:
        param2val = yaml.load(f, Loader=yaml.FullLoader)

    reps = len([fp for fp in group2predictions_file_paths[param_name] if fp.stem.endswith('_0')])
    step = group2predictions_file_paths[param_name][0].stem.split('_')[-1]
    # add info about conditions
    info = ''
    conditions = configs.Eval.conditions or ['is_official', 'is_reference', 'is_base', 'framework']
    for c in conditions:
        try:
            val = param2val[c]
        except KeyError:
            val = 'n/a'
        if isinstance(val, bool):
            val = int(val)
        info += f'{c}={val} '

    if show_step:
        return f'step={step} | n={reps} | {info}'
    else:
        return f'n={reps} | {info}'


def make_barplot(template2group_name2props: Dict[str, Dict[str, np.array]],
                 group2predictions_file_paths: Dict[str, List[Path]],
                 paradigm: str,
                 xlabel: str = '',
                 verbose: bool = False,
                 ):
    x = np.arange(1)

    num_axes = len(template2group_name2props)
    fig, axs = plt.subplots(num_axes, sharex='all', sharey='all',
                            dpi=configs.Figs.dpi, figsize=(8, 8))
    if num_axes == 1:
        # make axes iterable when there is only one axis only
        axs = [axs]

    for ax, template in zip(axs, template2group_name2props.keys()):
        group_name2props = template2group_name2props[template]
        num_models = len(group_name2props)
        space = 0.1  # between bars belonging to a single production category
        width = (1 / num_models) - (space / num_models)  # all bars in one category must fit within 1 x-axis unit
        edges = [width * i for i in range(num_models)]  # distances between x-ticks and bar-center
        colors = [f'C{i}' for i in range(num_models)]

        ax.set_xticks(x + (width * num_models / 2) - (width / 2))  # set tick exactly at center of a group of bars
        ax.set_xticklabels([])
        ax.set_xlabel(xlabel)
        ax.set_ylabel('Proportion', fontsize=configs.Figs.ax_font_size)
        ax.set_ylim([0, 1.0])
        ax.axhline(y=0.5, linestyle=':', color='grey', zorder=3)
        # ax.yaxis.grid()
        ax.set_title(f'{paradigm.replace("_", " ")}\n'
                     f'template={template}',
                     size=configs.Figs.ax_font_size)

        for edge, color, group_name in zip(edges, colors, group_name2props.keys()):
            avg = np.mean(group_name2props[group_name], axis=0).round(4)  # take across reps
            std = np.std(group_name2props[group_name], axis=0).round(4)

            if verbose:
                print(group_name)
                print(f'Plotting avg={avg}')
                print(f'Plotting std={std}')
                print()

            # plot all bars belonging to a single model group (same color)
            ax.bar(x + edge,
                   avg,
                   width,
                   yerr=std,
                   color=color,
                   zorder=3,
                   label=get_legend_label(group2predictions_file_paths, group_name))

    # legend
    plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.4), loc='upper left', frameon=False)

    # Hide x labels and tick labels for all but bottom plot.
    for ax in axs:
        ax.label_outer()

    plt.show()
