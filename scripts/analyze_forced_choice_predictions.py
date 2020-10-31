import importlib

from zorro import configs
from zorro.visualizer import Visualizer
from zorro.structure import prepare_data_for_barplot_forced_choice
from zorro.io import get_group2predictions_file_paths


STEP_SIZE = 10_000
MAX_STEP = 180_000

# chose one
TASK_NAMES = [
    'agreement_across_1_adjective',
    # 'agreement_across_2_adjectives',
    # 'agreement_across_PP',
    # 'agreement_across_RC',
    # 'agreement_in_1_verb_question',
    # 'agreement_in_2_verb_question',
]

for task_name in TASK_NAMES:
    # load module containing task-relevant objects
    s = importlib.import_module(f'zorro.{task_name}.score_forced_choice')

    for step in configs.Eval.custom_steps or list(range(0, MAX_STEP + STEP_SIZE, STEP_SIZE)):

        # load prediction files
        print('Loading data...')
        group2predictions_file_paths = get_group2predictions_file_paths(task_name, 'forced_choice', step)

        v = Visualizer(group2predictions_file_paths, step)

        # categorize productions into production categories
        print('Preparing data...')
        template2group_name2props = prepare_data_for_barplot_forced_choice(group2predictions_file_paths,
                                                                           task_name,
                                                                           s.templates,
                                                                           s.prediction_categories,
                                                                           s.categorize_by_template,
                                                                           s.categorize_predictions,
                                                                           )
        # plot
        v.make_barplot(s.prediction_categories, template2group_name2props, task_name)
