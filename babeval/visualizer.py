from typing import List, Dict, Optional, Tuple
import yaml
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

from babeval import configs

mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False


class Visualizer:
    def __init__(self, dpi=192):
        self.dpi = dpi
        self.figsize = (8, 8)
        self.ax_title_size = 10

    @staticmethod
    def get_legend_name(param_name, key):

        if key is None:
            return param_name

        if 'control' in param_name:
            return param_name

        if 'dummy' in param_name:
            return param_name

        path = configs.Dirs.predictions / param_name / 'param2val.yaml'
        with path .open('r') as f:
            param2val = yaml.load(f, Loader=yaml.FullLoader)

        res = f'step={configs.Eval.step} | n={configs.Eval.max_reps} | {key}={param2val[key]}'
        return res

    def make_barplot(self,
                     x_tick_labels: Tuple,
                     template2group_name2props: Dict[str, Dict[str, np.array]],
                     task_name: Optional[str] = None,
                     condition: Optional[str] = None,
                     verbose: bool = False):

        if condition is None:
            condition = configs.Eval.condition

        x = np.arange(len(x_tick_labels))
        width = 0.2

        num_axes = len(template2group_name2props)
        fig, axs = plt.subplots(num_axes, sharex='all', sharey='all',
                                dpi=self.dpi, figsize=self.figsize)
        if num_axes == 1:
            # make axes iterable when there is only one axis only
            axs = [axs]

        for ax, ax_title in zip(axs, template2group_name2props.keys()):
            ax.set_xticks(x + width)
            ax.set_xticklabels(x_tick_labels)
            ax.set_ylabel('Proportion')
            ax.axhline(y=0.5, linestyle=':', color='grey')
            ax.set_title(f'{task_name}: {ax_title}' if task_name else ax_title,
                         fontweight="bold", size=self.ax_title_size)

            group_name2props = template2group_name2props[ax_title]
            num_models = len(group_name2props)
            edges = [width * i for i in range(num_models)]
            colors = [f'C{i}' for i in range(num_models)]

            for edge, color, group_name in zip(edges, colors, group_name2props.keys()):
                avg = np.mean(group_name2props[group_name], axis=0).round(2)  # take average across rows
                std = np.std(group_name2props[group_name], axis=0).round(2)

                print(group_name)

                if verbose:
                    print(f'Plotting avg={avg}')
                    print(f'Plotting std={std}')
                    print()

                for i in range(std.shape[-1]):
                    if std[i] > avg[i]:
                        std[i] = avg[i]  # prevents space between bars and x-axis in figure

                ax.bar(x + edge,
                       avg,
                       width,
                       yerr=std,
                       color=color,
                       label=self.get_legend_name(group_name, condition))

        # legend
        plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.4), loc='upper left', frameon=False)

        # Hide x labels and tick labels for all but bottom plot.
        for ax in axs:
            ax.label_outer()

        plt.show()
