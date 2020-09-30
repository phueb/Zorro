from typing import List, Dict, Optional, Tuple
import yaml
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from pathlib import Path

from babeval import configs

mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False


class Visualizer:
    def __init__(self,
                 group2predictions_file_paths: Dict[str, List[Path]],
                 step: Optional[int] = None,
                 dpi=192):

        self.dpi = dpi
        self.ax_title_size = 10
        self.ax_label_size = 10

        self.group2predictions_file_paths = group2predictions_file_paths  # used to get number of reps

        self.step = step

    def get_legend_label(self, param_name):

        if 'control' in param_name:
            return param_name

        if configs.Eval.local_runs:
            runs_path = configs.Dirs.runs_local
        else:
            runs_path = configs.Dirs.runs_remote

        path = runs_path / param_name / 'param2val.yaml'
        with path .open('r') as f:
            param2val = yaml.load(f, Loader=yaml.FullLoader)

        reps = len(self.group2predictions_file_paths[param_name])

        # add info about conditions
        info = ''
        conditions = configs.Eval.conditions or ['param_name']
        for c in conditions:
            try:
                val = param2val[c]
            except KeyError:
                if c == 'architecture':
                    val = 'BabyBERT'
                else:
                    val = 'n/a'
            info += f'{c}={val} '

        res = f'step={self.step} | n={reps} | {info}'
        return res

    def make_barplot(self,
                     x_tick_labels: Tuple,
                     template2group_name2props: Dict[str, Dict[str, np.array]],
                     task_name: Optional[str] = None,
                     xlabel: str = '',
                     verbose: bool = False):

        x = np.arange(len(x_tick_labels))

        num_axes = len(template2group_name2props)
        fig, axs = plt.subplots(num_axes, sharex='all', sharey='all',
                                dpi=self.dpi, figsize=(8, 8))
        if num_axes == 1:
            # make axes iterable when there is only one axis only
            axs = [axs]

        for ax, ax_title in zip(axs, template2group_name2props.keys()):
            group_name2props = template2group_name2props[ax_title]
            num_models = len(group_name2props)
            space = 0.1  # between bars belonging to a single production category
            width = (1 / num_models) - (space / num_models)  # all bars in one category must fit within 1 x-axis unit
            edges = [width * i for i in range(num_models)]  # distances between x-ticks and bar-center
            colors = [f'C{i}' for i in range(num_models)]

            ax.set_xticks(x + (width * num_models / 2) - (width / 2))  # set tick exactly at center of a group of bars
            ax.set_xticklabels(x_tick_labels)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Proportion', fontsize=self.ax_label_size)
            ax.set_ylim([0, 1.0])
            ax.axhline(y=0.5, linestyle=':', color='grey')
            ax.set_title(f'{task_name}: {ax_title}' if task_name else ax_title,
                         fontweight="bold", size=self.ax_title_size)

            for edge, color, group_name in zip(edges, colors, group_name2props.keys()):
                avg = np.mean(group_name2props[group_name], axis=0).round(2)  # take average across rows
                std = np.std(group_name2props[group_name], axis=0).round(2)

                if verbose:
                    print(group_name)
                    print(f'Plotting avg={avg}')
                    print(f'Plotting std={std}')
                    print()

                for i in range(std.shape[-1]):
                    if std[i] > avg[i]:
                        std[i] = avg[i]  # prevents space between bars and x-axis in figure

                # plot all bars belonging to a single model group (same color)
                ax.bar(x + edge,
                       avg,
                       width,
                       yerr=std,
                       color=color,
                       label=self.get_legend_label(group_name))

        # legend
        plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.4), loc='upper left', frameon=False)

        # Hide x labels and tick labels for all but bottom plot.
        for ax in axs:
            ax.label_outer()

        plt.show()

    def make_scatterplot(self,
                         task_name: str,
                         group2xy: dict,
                         xlabel: str,
                         ylabel: str,
                         log_ten_scale: bool = True,
                         condition: Optional[str] = None,
                         ):

        if condition is None:
            condition = configs.Eval.condition

        group_names = list(group2xy.keys())
        num_groups = len(group_names)

        max_val = max([max(x) for x, y in group2xy.values()])
        if log_ten_scale:
            max_val = np.log10(max_val)

        # fig
        fig, axes = plt.subplots(1, num_groups, sharex='all', sharey='all',
                                 figsize=(10, 6), dpi=self.dpi)

        for group_name, (x, y) in group2xy.items():
            label = self.get_legend_label(group_name, condition)

            ax = axes[group_names.index(group_name)]
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.set_xlabel(xlabel, fontsize=self.ax_label_size)
            ax.set_ylabel(ylabel, fontsize=self.ax_label_size)
            ax.set_title(f'{task_name}\n{label}', size=self.ax_title_size)
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)

            ax.hist2d(np.log10(x) if log_ten_scale else x,
                      np.log10(y) if log_ten_scale else y,
                      range=[[0, max_val], [0, max_val]],
                      bins=100,
                      cmap=plt.cm.Greys)

            # plot identity line
            xl = [0, max_val]
            yl = [0, max_val]
            ax.plot(xl, yl, linestyle=':', c='black', zorder=3)

        plt.show()
