from typing import List, Dict, Optional
from dataclasses import dataclass, field
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from zorro import configs
from zorro.figs import get_legend_label


@dataclass
class ParadigmData:
    name: str
    group_name2template2curve: Dict[str, Dict[str, np.array]]  # by template
    group_names: List[str]
    group2prediction_file_paths: Dict[str, List[Path]]
    labels: List[str] = field(init=False)

    def __post_init__(self):
        self.labels = [get_legend_label(self.group2prediction_file_paths, gn)
                       for gn in self.group_names]


class Visualizer:
    def __init__(self,
                 num_rows: int = 2,
                 num_cols: int = 2,
                 label_last_x_tick_only: bool = True,
                 y_lims: Optional[List[float]] = None,
                 fig_size: int = (6, 6),
                 dpi: int = 192,
                 ):
        self.fig, self.ax_mat = plt.subplots(num_rows + 1, num_cols,
                                             figsize=fig_size,
                                             dpi=dpi,
                                             constrained_layout=True)

        self.x_axis_label = 'Training Step'
        self.y_axis_label = 'Proportion Correct'
        self.y_lims = y_lims or [0.5, 1.0]
        self.label_last_x_tick_only = label_last_x_tick_only
        self.x_ticks = configs.Eval.steps

        self.axes = enumerate(ax for ax in self.ax_mat.flatten())
        self.pds = []  # data, one for each axis/paradigm

    def update(self, pd: ParadigmData,
               ):

        self.pds.append(pd)

        # axis
        ax_id, ax = next(self.axes)
        ax.set_title(pd.name, fontsize=configs.Figs.ax_font_size)
        if ax_id % self.ax_mat.shape[1] == 0:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
        if ax_id >= self.ax_mat.shape[0] * (self.ax_mat.shape[1] - 1) - 1:
            ax.set_xlabel(self.x_axis_label, fontsize=configs.Figs.ax_font_size)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if self.label_last_x_tick_only:
            x_tick_labels = ['' if n < len(self.x_ticks) - 1 else i for n, i in enumerate(self.x_ticks)]
        else:
            x_tick_labels = self.x_ticks
        y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_ticks, fontsize=configs.Figs.tick_font_size)
        ax.set_xticks(self.x_ticks)
        ax.set_xticklabels(x_tick_labels, fontsize=configs.Figs.tick_font_size)
        ax.set_ylim(self.y_lims)

        # plot
        for gn, template2curves in pd.group_name2template2curve.items():
            ys = np.array([curve for curve in template2curves.values()]).mean(axis=0)
            ax.plot(self.x_ticks, ys, linewidth=2, color=f'C{pd.group_names.index(gn)}')

        self.fig.show()

    def plot_with_legend(self):

        labels = self.pds[-1].labels
        legend_elements = [Patch(facecolor=f'C{labels.index(label)}', label=label)
                           for label in labels]

        for ax_id, ax in self.axes:
            ax.axis('off')

        # legend
        self.fig.legend(handles=legend_elements,
                        loc='upper center',
                        bbox_to_anchor=(0.5, 0.2),  # distance from bottom-left (move up into  empty axes)
                        ncol=1,
                        frameon=False,
                        fontsize=configs.Figs.leg_font_size)

        self.fig.tight_layout()
        self.fig.show()

