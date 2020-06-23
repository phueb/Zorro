import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

class Visualizer:
    def __init__(self, dpi=192):
        self.dpi = dpi

    def make_barplot(self, x_tick_labels, title2file_name2props):

        x = np.arange(len(x_tick_labels))
        width = 0.2

        num_axes = len(title2file_name2props)
        fig, axs = plt.subplots(num_axes, sharex='all', sharey='all', dpi=self.dpi)
        if num_axes == 1:
            # make axes iterable when there is only one axis only
            axs = [axs]

        for ax, ax_title in zip(axs, title2file_name2props.keys()):
            ax.set_xticks(x + width)
            ax.set_xticklabels(x_tick_labels)
            ax.set_ylabel('Proportion')

            file_name2props = title2file_name2props[ax_title]
            num_models = len(file_name2props)
            edges = [width * i for i in range(num_models)]
            colors = [f'C{i}' for i in range(num_models)]

            for edge, color, file_name in zip(edges, colors, file_name2props.keys()):
                ax.bar(x + edge, file_name2props[file_name], width, color=color, label=file_name)
                ax.set_title(ax_title, fontweight="bold", size=8)

        # legend
        plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.5), loc='upper left', frameon=False)

        plt.show()

    def make_barplot_for_multiple_models(self, x_tick_labels, average_dict, std_dict, prediction_file_names):

        #single bar
        num_models = 5
        width = 0.2
        x = np.arange(len(x_tick_labels))

        num_axes = sum([len(i) for i in average_dict.values()])
        fig, axs = plt.subplots(num_axes, sharex=True, sharey=True, gridspec_kw={'hspace': 0}, dpi=self.dpi)

        fig.suptitle(f'Multiple BERTs Scoring \n Scoring {len(prediction_file_names)} Models', fontsize=8)

        #decompose dict
        avg_lst = []
        std_lst = []
        label_lst = []
        colors = [f'C{i}' for i in range(num_models)]

        for avg_title, std_title in zip(average_dict, std_dict):
            average_value = average_dict[avg_title].values()
            std_value = std_dict[std_title].values()
            label_dic = average_dict[avg_title].keys()

            for avg, std, label in zip(average_value, std_value, label_dic):
                avg_lst.append(avg)
                std_lst.append(std)
                label_lst.append(label)

        #plotting bars
        for i, avg, std, label in zip(range(num_axes), avg_lst, std_lst, label_lst):
            axs[i].set_xticks(x)
            axs[i].set_xticklabels(x_tick_labels)
            axs[i].set_ylabel('Proportion')

            axs[i].bar(x, avg, width, yerr = std, color = colors)
            axs[i].set_title(label, fontweight="bold", size=8)

        # Hide x labels and tick labels for all but bottom plot.
        for ax in axs:
            ax.label_outer()

        plt.show()

