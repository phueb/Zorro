import numpy as np
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self):
        pass

    def make_barplot(self, xtick_labels, fig_data, legend_labels):
        num_categories = np.arange(5)
        num_models = len(legend_labels)
        width = 0.2
        edges = [width * i for i in range(num_models)]
        colors = [f'C{i}' for i in range(num_models)]

        fig, axs = plt.subplots(3, sharex='all', sharey='all')
        for ax, ax_data in zip(axs, [fig_data[i] for i in ['1', '2', '3']]):
            ax.set_xticks(num_categories + width)
            ax.set_xticklabels(xtick_labels)

            for edge, color, label in zip(edges, colors, legend_labels):
                ax.bar(num_categories + edge, ax_data[label], width, color=color, label=label)
                ax.set_title(f'Sentence with {axs.tolist().index(ax) + 1} Adjective(s)', fontweight="bold", size=8)

        # legend
        plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.5), loc='upper left', frameon=False)

        fig.text(0.06, 0.5, 'proportion of total predictions that are in the category', ha='center', va='center',
                 rotation='vertical', size='small')


        plt.show()