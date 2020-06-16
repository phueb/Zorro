import numpy as np
from matplotlib import pyplot as plt

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

    def make_barplot_for_multiple_models(self, x_tick_labels, average_dict, std_dict):

        x = np.arange(len(x_tick_labels))
        width = 0.2
        num_axes = sum([len(i) for i in average_dict.values()])

        fig, axs = plt.subplots(num_axes, sharex='all', sharey='all', dpi=self.dpi)
        if num_axes == 1:
            axs = [axs]

        #ax_title = "average"
        for ax, ax_title in zip(axs, average_dict.keys()):
            ax.set_xticks(x + width)
            ax.set_xticklabels(x_tick_labels)
            ax.set_ylabel('Proportion')

            file_name2props = average_dict[ax_title]
            num_models = len(file_name2props)
            edges = [width * i for i in range(num_models)]
            colors = [f'C{i}' for i in range(num_models)]
            std = std_dict["standard deviation"].values()


            for edge, color, number, std_lst in zip(edges, colors, file_name2props.keys(), std):
                ax.bar(x + edge, file_name2props[number], width, yerr = std_lst, color=color)
                ax.set_title(ax_title, fontweight="bold", size=8)

        # # legend
        # plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.5), loc='upper left', frameon=False)

        plt.show()