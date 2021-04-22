import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

from zorro import configs


def plot_lines(ys: np.array,
               title: str,
               x_axis_label: str,
               y_axis_label: str,
               x_ticks: List[int],
               labels: List[str],
               y_lims: List[float] = (0, 1),
               baseline_frequency: Optional[float] = None,
               label_last_x_tick_only: bool = False,
               ):

    fig, ax = plt.subplots(1, figsize=(6, 4), dpi=163)
    plt.title(title, fontsize=configs.Figs.title_font_size)
    ax.set_ylabel(y_axis_label, fontsize=configs.Figs.ax_font_size)
    ax.set_xlabel(x_axis_label, fontsize=configs.Figs.ax_font_size)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(x_ticks)
    if label_last_x_tick_only:
        x_tick_labels = ['' if  n < len(x_ticks) - 1 else i for n, i in enumerate(x_ticks)]
    else:
        x_tick_labels = x_ticks
    ax.set_xticklabels(x_tick_labels, fontsize=configs.Figs.tick_font_size)
    if y_lims:
        ax.set_ylim(y_lims)

    # plot
    lines = []  # will have 1 list for each condition
    for n, y in enumerate(ys):
        print(x_ticks, y)
        line, = ax.plot(x_ticks, y, linewidth=2, color=f'C{n}')
        lines.append([line])

    if baseline_frequency is not None:
        line, = ax.plot(x_ticks, [baseline_frequency] * len(x_ticks), color='grey', ls='--')
        lines.append([line])
        labels.append(f'frequency baseline={baseline_frequency:.2f}')

    # legend
    plt.legend([l[0] for l in lines],
               labels,
               loc='upper center',
               bbox_to_anchor=(0.5, -0.3),
               ncol=2,
               frameon=False,
               fontsize=configs.Figs.leg_font_size)

    plt.show()