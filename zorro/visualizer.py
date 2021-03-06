from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import sem, t
from collections import defaultdict

from zorro import configs
from zorro.data import DataExperimental, DataBaseline
from zorro.scoring import count_correct_choices
from zorro.utils import shorten_tick_label

SHOW_PARTIAL_FIGURE = True  # whether to show partially completed figure while making large figure

MULTI_AXIS_LEG_NUM_COLS = 2  # 2 or 3 depending on space
MULTI_AXIS_LEG_OFFSET = 0.12
STANDALONE_LEG_OFFSET = 0.45
STANDALONE_FIG_SIZE = (4, 4)

# lines figure
Y_TICK_LABEL_FONTSIZE = 5


def make_ax_title(name: str):
    ax_title = name.replace('_', ' ')
    ax_title = ax_title.replace('coordinate', 'coord.')
    ax_title = ax_title.replace('structure', 'struct.')
    ax_title = ax_title.replace('prepositional', 'prep.')
    ax_title = ax_title.replace('agreement', 'agreem.')
    ax_title = ax_title.replace('determiner', 'det.')
    return ax_title


@dataclass
class ParadigmDataLines:
    steps: List[int]
    phenomenon: str
    paradigm: str
    group_names: List[str]
    labels: List[str]
    group_name2template2curve: Dict[str, Dict[str, List[float]]]  # grouped by template
    group_name2rep2curve: Dict[str, Dict[int, List[float]]]  # grouped by replication

    # init=False
    name: str = field(init=False)

    def __post_init__(self):
        self.name = f'{self.phenomenon}\n{self.paradigm}'


class VisualizerBase:
    def __init__(self,
                 phenomena_paradigms: List[Tuple[str, str]],
                 y_lims: Optional[List[float]] = None,
                 fig_size: int = (6, 5),
                 dpi: int = 300,
                 show_partial_figure: bool = SHOW_PARTIAL_FIGURE,
                 confidence: float = 0.90,
                 ):

        self.phenomena_paradigms = phenomena_paradigms
        self.y_lims = y_lims or [0.5, 1.01]
        self.show_partial_figure = show_partial_figure
        self.confidence = confidence

        # calc num rows needed
        self.num_cols = 5
        num_paradigms = len(phenomena_paradigms)
        num_paradigms_and_summary = num_paradigms + 1
        num_rows_for_data = num_paradigms_and_summary / self.num_cols
        num_rows_for_legend = 1
        self.num_rows = int(num_rows_for_data) + num_rows_for_legend
        self.num_rows += 1 if not num_rows_for_data.is_integer() else 0  # to fit summary

        self.fig, self.ax_mat = plt.subplots(self.num_rows, self.num_cols,
                                             figsize=fig_size,
                                             dpi=dpi,
                                             )

        self.y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        # remove all tick labels ahead of plotting to reduce space between subplots
        for ax in self.ax_mat.flatten():
            # y-axis
            y_ticks = []
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=configs.Figs.tick_font_size)
            # x-axis
            ax.set_xticks([])
            ax.set_xticklabels([])

        self.axes_for_legend = self.ax_mat[-1]
        self.axes = enumerate(ax for ax in self.ax_mat.flatten())
        self.pds = []  # data, one for each axis/paradigm

        self.last_step = None  # will be determined later


class VisualizerLines(VisualizerBase):
    def __init__(self,
                 step_size: int,
                 line_width: int = 1,
                 **kwargs
                 ):
        """plot accuracy across all training steps, for each paradigm"""

        super().__init__(**kwargs)

        self.line_width = line_width
        self.x_axis_label = 'Training Step'
        self.step_size = step_size

        self.y_axis_label = f'Accuracy\n+/- {self.confidence * 100}% CI'

        # score roberta-base output (only once for each paradigm)
        self.ax_kwargs_roberta_base = {'color': 'grey', 'linestyle': ':'}
        self.paradigm2roberta_base_accuracy = {}
        base_path = configs.Dirs.reference / 'huggingface_RoBERTa-base_Liu2019' / '0' / 'saves' / configs.Data.vocab_name
        for phenomenon, paradigm in self.phenomena_paradigms:
            model_output_path = base_path / f'probing_{phenomenon}-{paradigm}_results_500000.txt'
            data = DataExperimental(model_output_path, phenomenon, paradigm)
            num_correct = count_correct_choices(data)
            accuracy = num_correct / len(data.pairs)
            self.paradigm2roberta_base_accuracy[paradigm] = accuracy

        # score baseline (only once for each paradigm)
        self.ax_kwargs_baseline = {'color': 'grey', 'linestyle': '--'}
        self.paradigm2baseline_accuracy = {}
        for phenomenon, paradigm in self.phenomena_paradigms:
            data = DataBaseline('frequency baseline', phenomenon, paradigm)
            num_correct = count_correct_choices(data)
            accuracy = num_correct / len(data.pairs)
            self.paradigm2baseline_accuracy[paradigm] = accuracy

    def update(self,
               pd: ParadigmDataLines,
               ) -> None:
        """draw plot on one axis, corresponding to one paradigm"""

        self.pds.append(pd)

        self.last_step = pd.steps[-1]

        # get next axis
        ax_id, ax = next(self.axes)

        # title
        ax_title = make_ax_title(pd.name)
        ax.set_title(ax_title, fontsize=configs.Figs.title_font_size)

        # y axis
        if ax_id % self.ax_mat.shape[1] == 0:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
            y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=Y_TICK_LABEL_FONTSIZE)

        # x-axis
        if ax_id >= (self.num_rows - 1 - 1) * self.num_cols:   # -1 for figure legend, -1 to all axes in row
            ax.set_xlabel(self.x_axis_label, fontsize=configs.Figs.ax_font_size)
            ax.set_xticks([pd.steps[-1]])
            ax.set_xticklabels([shorten_tick_label(pd.steps[-1])], fontsize=configs.Figs.tick_font_size)
        # axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        # plot
        for gn, rep2curve in pd.group_name2rep2curve.items():
            color = f'C{pd.group_names.index(gn)}'
            curves = np.vstack([rep2curve[rep] for rep in rep2curve])  # one curve for each replication
            curves = curves[~(np.isnan(curves))].reshape((len(curves), -1))  # remove nans (step may be too large)
            x = pd.steps
            y = curves.mean(axis=0)
            ax.plot(x, y, linewidth=self.line_width, color=color)

            # plot the margin of error (shaded region)
            n = len(curves)
            h = sem(curves, axis=0) * t.ppf((1 + self.confidence) / 2, n - 1)  # margin of error
            ax.fill_between(x, y + h, y - h, alpha=0.2, color=color)

            # plot roberta-base accuracy as a horizontal line
            y_roberta_base = [self.paradigm2roberta_base_accuracy[pd.paradigm]] * len(x)
            ax.plot(x, y_roberta_base, linewidth=self.line_width, **self.ax_kwargs_roberta_base)

            # plot roberta-base accuracy as a horizontal line
            y_baseline = [self.paradigm2baseline_accuracy[pd.paradigm]] * len(x)
            ax.plot(x, y_baseline, linewidth=self.line_width, **self.ax_kwargs_baseline)

        # plot legend only once to prevent degradation in text quality due to multiple plotting
        if ax_id == 0:
            self._plot_legend(offset_from_bottom=MULTI_AXIS_LEG_OFFSET,
                              ncol=MULTI_AXIS_LEG_NUM_COLS)
            self.fig.show()

        if self.show_partial_figure:
            self.fig.tight_layout()
            self.fig.show()

    def plot_summary(self):
        """plot average accuracy (across all paradigms) in last axis"""

        # get next axis in multi-axis figure and plot summary there
        ax_id, ax = next(self.axes)
        self._plot_summary_on_axis(ax,
                                   label_y_axis=ax_id % self.ax_mat.shape[1] == 0,
                                   use_title=True)

        # remove axis decoration from any remaining axis
        for ax_id, ax in self.axes:
            ax.axis('off')

        # also plot summary in standalone figure
        fig_standalone, (ax1, ax2) = plt.subplots(2, figsize=STANDALONE_FIG_SIZE, dpi=300)
        self._plot_summary_on_axis(ax1,
                                   label_y_axis=True,
                                   use_title=False)
        ax2.axis('off')
        self._plot_legend(offset_from_bottom=STANDALONE_LEG_OFFSET, fig=fig_standalone)

        # show
        self.fig.show()
        fig_standalone.show()

    def _plot_summary_on_axis(self,
                              ax: plt.axis,
                              label_y_axis: bool,
                              use_title: bool,
                              ):
        """used to plot summary on multi-axis figure, or in standalone figure"""

        # axis
        if use_title:
            ax.set_title('Average', fontsize=configs.Figs.title_font_size)
            y_axis_label = self.y_axis_label
        else:
            y_axis_label = f'Average {self.y_axis_label}'
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        # x-axis
        ax.set_xticks([self.last_step])
        ax.set_xticklabels([shorten_tick_label(self.last_step)], fontsize=configs.Figs.tick_font_size)
        ax.set_xlabel(self.x_axis_label, fontsize=configs.Figs.ax_font_size)

        # y axis
        if label_y_axis:
            ax.set_ylabel(y_axis_label, fontsize=configs.Figs.ax_font_size)
            ax.set_yticks(self.y_ticks)
            ax.set_yticklabels(self.y_ticks, fontsize=configs.Figs.tick_font_size)
        else:
            ax.set_ylabel('', fontsize=configs.Figs.ax_font_size)
            ax.set_yticks([])
            ax.set_yticklabels([], fontsize=configs.Figs.tick_font_size)

        # collect curves for each replication across all paradigms
        gn2rep2curves_by_pd = defaultdict(dict)
        for pd in self.pds:
            for gn, rep2curve in pd.group_name2rep2curve.items():
                for rep, curve in rep2curve.items():
                    # this curve is performance collapsed across template and for a unique rep and paradigm
                    gn2rep2curves_by_pd[gn].setdefault(rep, []).append(curve)

        # plot
        for gn, rep2curves_by_pd in gn2rep2curves_by_pd.items():
            # average across paradigms
            rep2curve_avg_across_pds = {rep: np.array(curves_by_pd).mean(axis=0)
                                        for rep, curves_by_pd in rep2curves_by_pd.items()}
            curves = np.array([rep2curve_avg_across_pds[rep] for rep in rep2curve_avg_across_pds])  # one for each rep

            color = f'C{self.pds[0].group_names.index(gn)}'
            x = np.arange(0, self.last_step + self.step_size, self.step_size)

            # plot averages for BabyBERTa
            y = np.array(curves).mean(axis=0)
            ax.plot(x, y, linewidth=self.line_width, color=color)

            # plot average for RoBERTa-base
            y_roberta_base = np.repeat(np.mean(list(self.paradigm2roberta_base_accuracy.values())), len(x))
            ax.plot(x, y_roberta_base, linewidth=self.line_width, **self.ax_kwargs_roberta_base)

            # plot average for frequency baseline
            y_baseline = np.repeat(np.mean(list(self.paradigm2baseline_accuracy.values())), len(x))
            ax.plot(x, y_baseline, linewidth=self.line_width, **self.ax_kwargs_baseline)

            # plot the margin of error (shaded region)
            n = len(curves)
            h = sem(curves, axis=0) * t.ppf((1 + self.confidence) / 2, n - 1)  # margin of error
            ax.fill_between(x, y + h, y - h, alpha=0.2, color=color)

            # printout
            if use_title:  # to prevent printing summary twice
                print(f'{gn} avg acc at step {self.last_step} = {y[-1]:.3f}')

        if use_title:
            y_roberta_base = np.mean(list(self.paradigm2roberta_base_accuracy.values()))
            print(f'roberta-base Liu2019 avg acc at step {self.last_step} = {y_roberta_base:.3f}')

    def _plot_legend(self,
                     offset_from_bottom: float,
                     fig: Optional[plt.Figure] = None,
                     ncol: int = 1,
                     ):

        if fig is None:
            fig = self.fig

        labels = self.pds[-1].labels
        legend_elements = [Line2D([0], [0], color=f'C{n}', label=label) for n, label in enumerate(labels)]
        legend_elements.append(Line2D([0], [0], label='RoBERTa-base pre-trained by Liu et al. 2019', **self.ax_kwargs_roberta_base))
        legend_elements.append(Line2D([0], [0], label='frequency baseline', **self.ax_kwargs_baseline))

        for ax in self.axes_for_legend:
            ax.axis('off')

        # legend
        fig.legend(handles=legend_elements,
                   loc='upper center',
                   bbox_to_anchor=(0.5, offset_from_bottom),
                   ncol=ncol,
                   frameon=False,
                   fontsize=configs.Figs.leg_font_size)
