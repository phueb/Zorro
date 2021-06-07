from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import sem, t
from collections import defaultdict

from zorro import configs
from zorro.data import DataExperimental, DataBaseline
from zorro.scoring import count_correct_choices
from zorro.utils import get_reps, shorten_tick_labels, get_legend_label


MULTI_AXIS_LEG_OFFSET = 0.11
SUMMARY_LEG_OFFSET = 0.42


def shorten(name: str):
    """make name of phenomenon shorter to fit in figure"""
    name = name.replace('demonstrative', 'det.')
    return name


@dataclass
class ParadigmDataLines:
    phenomenon: str
    paradigm: str
    group_name2model_output_paths: Dict[str, List[Path]]
    group_name2template2curve: Dict[str, Dict[str, List[float]]]  # grouped by template
    group_name2rep2curve: Dict[str, Dict[int, List[float]]]  # grouped by replication

    # init=False
    labels: List[str] = field(init=False)
    name: str = field(init=False)
    group_names: List[str] = field(init=False)

    def __post_init__(self):
        self.labels = [get_legend_label(gn, reps=get_reps(model_output_paths, step=0))
                       for gn, model_output_paths in self.group_name2model_output_paths.items()]
        self.name = f'{shorten(self.phenomenon)}\n{self.paradigm}'
        self.group_names = [gn for gn in self.group_name2model_output_paths]


@dataclass
class ParadigmDataBars:
    phenomenon: str
    paradigm: str
    group_name2model_output_paths: Dict[str, List[Path]]
    group_name2template2acc: Dict[str, Dict[str, List[float]]]  # grouped by template
    group_name2rep2acc: Dict[str, Dict[int, List[float]]]  # grouped by replication

    # init=False
    labels: List[str] = field(init=False)
    name: str = field(init=False)
    group_names: List[str] = field(init=False)

    def __post_init__(self):
        self.labels = [get_legend_label(gn, reps=get_reps(model_output_paths, step=None))
                       for gn, model_output_paths in self.group_name2model_output_paths.items()]
        self.name = f'{shorten(self.phenomenon)}\n{self.paradigm}'
        self.group_names = [gn for gn in self.group_name2model_output_paths]


class VisualizerBase:
    def __init__(self,
                 phenomena_paradigms: List[Tuple[str, str]],
                 y_lims: Optional[List[float]] = None,
                 fig_size: int = (6, 6),
                 dpi: int = 300,
                 show_partial_figure: bool = False,
                 confidence: float = 0.90,
                 ):

        self.phenomena_paradigms = phenomena_paradigms
        self.y_lims = y_lims or [0.5, 1.01]
        self.show_partial_figure = show_partial_figure
        self.confidence = confidence

        # calc num rows needed
        self.num_cols = 4
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


class VisualizerLines(VisualizerBase):
    def __init__(self,
                 label_last_x_tick_only: bool = True,
                 line_width: int = 1,
                 **kwargs
                 ):
        """plot accuracy across all training steps, for each paradigm"""

        super().__init__(**kwargs)

        self.line_width = line_width
        self.x_axis_label = 'Training Step'
        self.x_ticks = configs.Eval.steps

        self.y_axis_label = f'Accuracy\n+/- {self.confidence * 100}% CI'

        if label_last_x_tick_only:
            self.x_tick_labels = ['' if xi != self.x_ticks[-1] else xi for xi in self.x_ticks]
        else:
            self.x_tick_labels = self.x_ticks

        # score roberta-base output (only once for each paradigm)
        self.ax_kwargs_roberta_base = {'color': 'grey', 'linestyle': ':'}
        self.paradigm2roberta_base_accuracy = {}
        base_path = configs.Dirs.runs_local / 'huggingface_Roberta-base_160GB' / '0' / 'saves' / 'forced_choice' / '8192'
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

        # get next axis
        ax_id, ax = next(self.axes)
        ax_title = pd.name.replace('_', ' ')
        ax.set_title(ax_title, fontsize=configs.Figs.title_font_size)
        # y axis
        if ax_id % self.ax_mat.shape[1] == 0:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
            y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=configs.Figs.tick_font_size)

        # x-axis
        if ax_id >= (self.num_rows - 1 - 1) * self.num_cols:   # -1 for figure legend, -1 to all axes in row
            ax.set_xlabel(self.x_axis_label, fontsize=configs.Figs.ax_font_size)
            ax.set_xticks(self.x_ticks)
            ax.set_xticklabels(shorten_tick_labels(self.x_tick_labels), fontsize=configs.Figs.tick_font_size)
        # axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        # plot
        for gn, rep2curve in pd.group_name2rep2curve.items():
            color = f'C{pd.group_names.index(gn)}'
            curves = np.array([rep2curve[rep] for rep in rep2curve])  # one curve for each replication
            curves = curves[~(np.isnan(curves))].reshape((len(curves), -1))  # remove nans (step may be too large)
            x = self.x_ticks[:curves.shape[1]]
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
            self._plot_legend(offset_from_bottom=MULTI_AXIS_LEG_OFFSET)
            self.fig.show()

        if self.show_partial_figure:
            self.fig.tight_layout()
            self.fig.show()

    def plot_summary(self):
        """plot average accuracy (across all paradigms) in last axis"""

        # get next axis in multi-axis figure and plot summary there
        ax_id, ax = next(self.axes)
        self._plot_summary_on_axis(ax, label_y_axis=ax_id % self.ax_mat.shape[1] == 0)
        self.fig.show()

        # also plot summary in standalone figure
        fig_standalone, (ax1, ax2) = plt.subplots(2, figsize=(3, 3), dpi=300)
        self._plot_summary_on_axis(ax1, label_y_axis=True)
        ax2.axis('off')
        self._plot_legend(offset_from_bottom=SUMMARY_LEG_OFFSET, fig=fig_standalone)
        fig_standalone.show()

    def _plot_summary_on_axis(self, ax: plt.axis,
                              label_y_axis: bool,
                              ):
        """used to plot summary on multi-axis figure, or in standalone figure"""

        # axis
        ax.set_title('Average', fontsize=configs.Figs.title_font_size)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        # x-axis
        ax.set_xticks(self.x_ticks)
        ax.set_xticklabels(shorten_tick_labels(self.x_tick_labels), fontsize=configs.Figs.tick_font_size)
        ax.set_xlabel(self.x_axis_label, fontsize=configs.Figs.ax_font_size)

        # y axis
        if label_y_axis:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
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

            # plot averages for BabyBERTa
            color = f'C{self.pds[0].group_names.index(gn)}'
            y = np.array(curves).mean(axis=0)
            x = self.x_ticks[:len(y)]
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

        # remove axis decoration from any remaining axis
        for ax_id, ax in self.axes:
            ax.axis('off')

    def _plot_legend(self,
                     offset_from_bottom: float,
                     fig: Optional[plt.Figure] = None,
                     ):

        if fig is None:
            fig = self.fig

        labels = self.pds[-1].labels
        legend_elements = [Line2D([0], [0], color=f'C{n}', label=label) for n, label in enumerate(labels)]
        legend_elements.append(Line2D([0], [0], label='RoBERTa-base', **self.ax_kwargs_roberta_base))
        legend_elements.append(Line2D([0], [0], label='frequency baseline', **self.ax_kwargs_baseline))

        for ax in self.axes_for_legend:
            ax.axis('off')

        # legend
        fig.legend(handles=legend_elements,
                   loc='upper center',
                   bbox_to_anchor=(0.5, offset_from_bottom),
                   ncol=1,
                   frameon=False,
                   fontsize=configs.Figs.leg_font_size)


class VisualizerBars(VisualizerBase):
    def __init__(self,
                 verbose: bool = True,
                 **kwargs
                 ):
        """plot accuracy at last training step only, for each paradigm"""

        self.verbose = verbose
        self.width = 0.2  # between bars  # TODO remove this

        self.y_axis_label = 'Accuracy'  #

        super().__init__(**kwargs)

    def update(self,
               pd: ParadigmDataBars,
               ) -> None:
        """draw plot on one axis, corresponding to one paradigm"""

        self.pds.append(pd)

        # get next axis
        ax_id, ax = next(self.axes)
        ax_title = pd.name.replace("_"," ")
        ax.set_title(ax_title, fontsize=configs.Figs.title_font_size)

        # y axis
        if ax_id % self.ax_mat.shape[1] == 0:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
            y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=configs.Figs.tick_font_size)
        # x-axis
        ax.set_xticks([])
        ax.set_xticklabels([])

        # axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        group_names = [gn for gn in pd.group_name2rep2acc.keys()]
        num_groups = len(group_names)
        edges = [self.width * i for i in range(num_groups)]  # distances between x-ticks and bar-center
        colors = [f'C{i}' for i in range(num_groups)]

        x = np.arange(1)

        # plot
        for edge, color, group_name in zip(edges, colors, group_names):
            rep2acc = pd.group_name2rep2acc[group_name]
            accuracies = [acc for acc in rep2acc.values()]
            y = np.mean(accuracies, axis=0)  # take average across reps

            # margin of error
            n = len(accuracies)
            h = sem(accuracies, axis=0) * t.ppf((1 + self.confidence) / 2, n - 1)  # margin of error

            # plot all bars belonging to a single model group (same color)
            ax.bar(x + edge,
                   y,
                   self.width,
                   yerr=h,
                   color=color,
                   zorder=3,
                   )

        # plot legend only once to prevent degradation in text quality due to multiple plotting
        if ax_id == 0:
            self._plot_legend(offset_from_bottom=MULTI_AXIS_LEG_OFFSET)

        if self.show_partial_figure:
            self.fig.tight_layout()
            self.fig.show()

    def plot_summary(self):
        """plot average accuracy (across all paradigms) in last axis"""

        # get next axis in multi-axis figure and plot summary there
        ax_id, ax = next(self.axes)
        self._plot_summary_on_axis(ax, label_y_axis=ax_id % self.ax_mat.shape[1] == 0)
        self.fig.show()

        # also plot summary in standalone figure
        fig_standalone, (ax1, ax2) = plt.subplots(2, figsize=(3, 3), dpi=300)
        self._plot_summary_on_axis(ax1, label_y_axis=True)
        ax2.axis('off')
        fig_standalone.subplots_adjust(top=0.1, bottom=0.01)
        self._plot_legend(offset_from_bottom=SUMMARY_LEG_OFFSET, fig=fig_standalone)
        fig_standalone.show()

    def _plot_summary_on_axis(self,
                              ax: plt.axis,
                              label_y_axis: bool,
                              ):
        """used to plot summary on multi-axis figure, or in standalone figure"""

        # axis
        ax.set_title('Average', fontsize=configs.Figs.title_font_size)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(self.y_lims)

        # x-axis
        ax.set_xticks([])
        ax.set_xticklabels([])
        # y axis
        if label_y_axis:
            ax.set_ylabel(self.y_axis_label, fontsize=configs.Figs.ax_font_size)
            ax.set_yticks(self.y_ticks)
            ax.set_yticklabels(self.y_ticks, fontsize=configs.Figs.tick_font_size)
        else:
            y_ticks = []
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_ticks, fontsize=configs.Figs.tick_font_size)

        # collect last_accuracy for each replication across all paradigms
        gn2rep2accuracies_by_pd = defaultdict(dict)
        for pd in self.pds:
            for gn, rep2acc in pd.group_name2rep2acc.items():
                for rep, acc in rep2acc.items():
                    gn2rep2accuracies_by_pd[gn].setdefault(rep, []).append(acc)
        group_names = [gn for gn in gn2rep2accuracies_by_pd]
        num_groups = len(group_names)
        edges = [self.width * i for i in range(num_groups)]  # distances between x-ticks and bar-center
        colors = [f'C{i}' for i in range(num_groups)]
        x = np.arange(1)

        # plot
        for edge, color, group_name in zip(edges, colors, group_names):
            rep2accuracies_by_pd = gn2rep2accuracies_by_pd[group_name]

            # average across paradigms
            rep2acc_avg_across_pds = {rep: np.array(accuracies_by_pd).mean(axis=0)
                                      for rep, accuracies_by_pd in rep2accuracies_by_pd.items()}
            accuracies = np.array([rep2acc_avg_across_pds[rep] for rep in rep2acc_avg_across_pds])  # one for each rep
            y = accuracies.mean()

            # margin of error
            n = len(accuracies)
            h = sem(accuracies, axis=0) * t.ppf((1 + self.confidence) / 2, n - 1)  # margin of error

            # plot all bars belonging to a single model group (same color)
            ax.bar(x + edge,
                   y,
                   self.width,
                   yerr=h,
                   color=color,
                   zorder=3,
                   )

            # print average performance by group
            print(f'{group_name:<96} y={y:.2f}')

        # remove axis decoration from any remaining axis
        for ax_id, ax in self.axes:
            ax.axis('off')

    def _plot_legend(self,
                     offset_from_bottom: float,
                     fig: Optional[plt.Figure] = None,
                     ):

        if fig is None:
            fig = self.fig

        labels = self.pds[-1].labels
        legend_elements = [Line2D([0], [0], color=f'C{n}', label=label) for n, label in enumerate(labels)]

        for ax in self.axes_for_legend:
            ax.axis('off')

        # legend
        fig.legend(handles=legend_elements,
                   loc='upper center',
                   bbox_to_anchor=(0.5, offset_from_bottom),
                   ncol=1,
                   frameon=False,
                   fontsize=configs.Figs.leg_font_size)
