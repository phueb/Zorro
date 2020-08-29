import importlib

from babeval import configs
from babeval.visualizer import Visualizer
from babeval.structure import prepare_data_for_barplot_forced_choice
from babeval.io import get_group2predictions_file_paths


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
    s = importlib.import_module(f'babeval.{task_name}.score_forced_choice')

    for step in configs.Eval.custom_steps or list(range(0, MAX_STEP + STEP_SIZE, STEP_SIZE)):

        # load prediction files
        group2predictions_file_paths = get_group2predictions_file_paths(task_name, 'forced_choice', step)

        v = Visualizer(group2predictions_file_paths, step)

        # categorize productions into production categories
        template2group_name2props = prepare_data_for_barplot_forced_choice(group2predictions_file_paths,
                                                                           task_name,
                                                                           s.templates,
                                                                           s.prediction_categories,
                                                                           s.categorize_by_template,
                                                                           s.categorize_predictions,
                                                                           )
        # plot
        v.make_barplot(s.prediction_categories, template2group_name2props, task_name)
