import numpy as np
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self, dpi=192):
        self.dpi = dpi
        self.figsize = (10, 10)

    def make_barplot(self, x_tick_labels, template2group_name2props):

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

            file_name2props = template2group_name2props[ax_title]
            num_models = len(file_name2props)
            edges = [width * i for i in range(num_models)]
            colors = [f'C{i}' for i in range(num_models)]

            for edge, color, file_name in zip(edges, colors, file_name2props.keys()):
                avg = np.mean(file_name2props[file_name], axis=0).round(2)  # take average across rows
                std = np.std(file_name2props[file_name], axis=0).round(2)

                print(f'Plotting avg={avg}')
                print(f'Plotting std={std}')
                print()

                for i in range(std.shape[-1]):
                    if std[i] > avg[i]:
                        std[i] = avg[i]  # prevents space between bars and x-axis in figure

                ax.bar(x + edge, avg, width, yerr=std, color=color, label=file_name)
                ax.set_title(ax_title, fontweight="bold", size=8)

        # legend
        plt.legend(prop={'size': 8}, bbox_to_anchor=(0.0, -0.5), loc='upper left', frameon=False)

        # Hide x labels and tick labels for all but bottom plot.
        for ax in axs:
            ax.label_outer()

        plt.show()
