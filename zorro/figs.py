import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Union, Optional
import yaml
from pathlib import Path
from matplotlib import rcParams

from zorro import configs

rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False


def shorten_tick_labels(labels: List[Union[str,int]],
                        ) -> List[str]:
    return [str(label)[:-3] + 'K' if str(label).endswith('000') else label
            for label in labels]


def get_legend_label(group2model_output_paths,
                     group_name,
                     conditions: Optional[List[str]] = None,
                     add_group_name: bool = False,
                     ) -> str:
    if group_name.endswith('frequency baseline'):
        return 'frequency baseline'

    if configs.Eval.local_runs:
        runs_path = configs.Dirs.runs_local
    else:
        runs_path = configs.Dirs.runs_remote

    param2val = load_param2val(group_name, runs_path)

    if configs.Eval.n_override:
        reps = configs.Eval.n_override  # cheating a little bit when reps is not perfectly consistent across groups
        print(f'WARNING: Set n manually to {configs.Eval.n_override}')
    else:
        reps = len([fp for fp in group2model_output_paths[group_name] if fp.stem.endswith('_0')])

    # make label
    res = f'BabyBERTa | n={reps} | '
    for c in conditions or configs.Eval.conditions:
        if c == 'load_from_checkpoint' and param2val[c] != 'none':
            param2val_previous = load_param2val(param2val[c], runs_path)
            res += f'previously trained on={param2val_previous["corpora"]} '
            continue
        try:
            val = param2val[c]
        except KeyError:
            val = 'n/a'
        if isinstance(val, bool):
            val = int(val)
        res += f'{c}={val} '

    if add_group_name:
        res += ' | ' + group_name

    return res


def load_param2val(group_name, runs_path):
    path = runs_path / group_name / 'param2val.yaml'
    with path.open('r') as f:
        param2val = yaml.load(f, Loader=yaml.FullLoader)
    return param2val


def show_barplot(template2group_name2accuracies: Dict[str, Dict[str, np.array]],
                 group2model_output_paths: Dict[str, List[Path]],
                 paradigm: str,
                 step: str,
                 xlabel: str = '',
                 verbose: bool = False,
                 conditions: Optional[List[str]] = None,
                 ):
    x = np.arange(1)

    num_axes = len(template2group_name2accuracies)
    fig, axs = plt.subplots(num_axes, sharex='all', sharey='all',
                            dpi=163, figsize=(8, 8))
    if num_axes == 1:
        # make axes iterable when there is only one axis only
        axs = [axs]

    for ax, template in zip(axs, template2group_name2accuracies.keys()):
        group_name2accuracies = template2group_name2accuracies[template]
        num_models = len(group_name2accuracies)
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
                     f'template={template}\n'
                     f'step={step}',
                     size=configs.Figs.ax_font_size)

        for edge, color, group_name in zip(edges, colors, group_name2accuracies.keys()):
            avg = np.mean(group_name2accuracies[group_name], axis=0).round(4)  # take across reps
            std = np.std(group_name2accuracies[group_name], axis=0).round(4)

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
                   label=get_legend_label(group2model_output_paths, group_name, conditions))

    # legend
    plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.4), loc='upper left', frameon=False)

    # Hide x labels and tick labels for all but bottom plot.
    for ax in axs:
        ax.label_outer()

    plt.show()
