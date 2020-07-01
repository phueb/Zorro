import importlib

from babeval.visualizer import Visualizer
from babeval.prepare import prepare_data_for_plotting


task_names = [
    'agreement_across_adjectives',
    'agreement_across_PP',
    'agreement_across_RC',
    'agreement_in_question',
]

# score + visualize productions for each task
v = Visualizer()
for task_name in task_names:
    s = importlib.import_module(f'babeval.{task_name}.score')

    # categorize productions into production categories
    template2group_name2props = prepare_data_for_plotting(s.group2predictions_file_paths,
                                                          s.templates,
                                                          s.prediction_categories,
                                                          s.categorize_by_template,
                                                          s.categorize_predictions,
                                                          s.print_stats)
    # plot
    v.make_barplot(s.prediction_categories, template2group_name2props, s.task_name)

    ###

    # categorize productions into bi-gram percentile categories  # TODO similar as above but categories are percentiles
    template2group_name2props = prepare_data_for_plotting(s.group2predictions_file_paths,
                                                          s.templates,
                                                          s.prediction_categories,
                                                          s.categorize_by_template,
                                                          s.categorize_predictions,
                                                          s.print_stats)

    # plot
    v.make_barplot(s.prediction_categories, template2group_name2props, s.task_name)
