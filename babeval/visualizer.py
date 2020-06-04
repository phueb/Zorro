import numpy as np
from matplotlib import pyplot as plt, patches as mpatches


class Visualizer:
    def __init__(self):
        pass

    def make_barplot(self, xtick_labels, y1, y2, y3, z1, z2, z3, legend_labels):
        ind = np.arange(5)
        width = 0.4

        fig, axs = plt.subplots(3, sharex=True, sharey=True)

        for i in range(3):
            axs[i].set_xticks(ind + width)
            axs[i].set_xticklabels(xtick_labels)

        # for axs[0]
        axs[0].bar(ind, y1, width, color='xkcd:tomato', align='center')
        axs[0].bar(ind + (width / 2), z1, width, color='xkcd:darkblue', align='edge')
        # for axs[1]
        axs[1].bar(ind, y2, width, color='xkcd:tomato', align='center')
        axs[1].bar(ind + (width / 2), z2, width, color='xkcd:darkblue', align='edge')
        # for axs[2]
        axs[2].bar(ind, y3, width, color='xkcd:tomato', align='center')
        axs[2].bar(ind + (width / 2), z3, width, color='xkcd:darkblue', align='edge')
        # set titles
        axs[0].set_title('Sentence with Single Adjective', fontweight="bold", size=8)
        axs[1].set_title('Sentence with Two Adjectives', fontweight="bold", size=8)
        axs[2].set_title('Sentence with Three Adjectives', fontweight="bold", size=8)

        blue_patch = mpatches.Patch(color='xkcd:tomato', label=legend_labels[0])
        green_patch = mpatches.Patch(color='xkcd:darkblue', label=legend_labels[1])
        fig.legend(handles=[blue_patch, green_patch], prop={'size': 6})

        fig.text(0.06, 0.5, 'proportion of total predictions that are in the category', ha='center', va='center',
                 rotation='vertical', size='small')

        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()

        plt.savefig("agreement_across_adjectives" + '.png', dpi=700)

        plt.show()