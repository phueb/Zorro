import numpy as np
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self):
        pass

    def make_barplot(self, x_tick_labels, title2file_name2props):

        x = np.arange(len(x_tick_labels))
        width = 0.2

        fig, axs = plt.subplots(len(title2file_name2props), sharex='all', sharey='all')
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