import importlib
from collections import defaultdict
import numpy as np

from zorro import configs
from zorro.visualizer import Visualizer
from zorro.prepare import prepare_data_for_barplot_forced_choice
from zorro.io import get_group2predictions_file_paths
from zorro.figs import plot_lines


# chose one
TASK_NAMES = [
    # 'agreement_across_1_adjective',
    # 'agreement_across_2_adjectives',
    # 'agreement_across_PP',
    # 'agreement_across_RC',
    # 'agreement_in_1_verb_question',
    # 'agreement_in_2_verb_question',
    'agreement_between_neighbors',
]

for task_name in TASK_NAMES:
    # load module containing task-relevant objects
    s = importlib.import_module(f'zorro.{task_name}.score_forced_choice')

    # for line plot
    template2group_name2curve = defaultdict(dict)

    for step in configs.Eval.steps:

        # load prediction files
        print('Loading data...')
        group2predictions_file_paths = get_group2predictions_file_paths(task_name, 'forced_choice', step)

        v = Visualizer(group2predictions_file_paths)

        # categorize choice as correct or false
        print('Preparing data...')
        template2group_name2props = prepare_data_for_barplot_forced_choice(group2predictions_file_paths,
                                                                           task_name,
                                                                           s.templates,
                                                                           s.prediction_categories,
                                                                           s.categorize_by_template,
                                                                           s.grammar_checker,
                                                                           )
        # plot
        v.make_barplot(s.prediction_categories,
                       template2group_name2props,
                       task_name,
                       verbose=True,
                       )

        # collect for line plot
        for template, group_name2props in template2group_name2props.items():
            for group_name, props in group_name2props.items():
                curve_i = np.mean(props)  # the mean proportion of a group at one location on curve
                template2group_name2curve[template].setdefault(group_name, []).append(curve_i)

    # plot developmental trajectory of each model
    for template, group_name2curve in template2group_name2curve.items():
        plot_lines(ys=np.array([curve for curve in group_name2curve.values()]),
                   title=f'Learning Trajectories\ntemplate={template}',
                   x_axis_label='Training Step',
                   y_axis_label='Proportion Correct',
                   x_ticks=configs.Eval.steps,
                   labels=list(group_name2curve.keys()),
                   )
