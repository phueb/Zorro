import importlib

from babeval.visualizer import Visualizer
from babeval.prepare import prepare_data_for_plotting
from babeval.bigrams import categorize_left_bigrams, categorize_right_bigrams, bigram_frequency_percentiles
from babeval.io import get_group2predictions_file_paths

ANALYZE_PREDICTION_CATEGORIES = False
ANALYZE_LEFT_BIGRAM_FREQUENCY_PERCENTILES = False
ANALYZE_RIGHT_BIGRAM_FREQUENCY_PERCENTILES = True

STEPS = [0, 20_000, 40_000, 60_000, 80_000, 100_000, 120_000, 140_000, 160_000, 180_000]

task_names = [
    'agreement_across_adjectives',
    # 'agreement_across_PP',
    # 'agreement_across_RC',
    # 'agreement_in_question',
]

for task_name in task_names:
    # load module containing task-relevant objects
    s = importlib.import_module(f'babeval.{task_name}.score')

    for step in STEPS:
        v = Visualizer(step)

        # load prediction files
        group2predictions_file_paths = get_group2predictions_file_paths(task_name, step)

        if ANALYZE_PREDICTION_CATEGORIES:

            # categorize productions into production categories
            template2group_name2props = prepare_data_for_plotting(group2predictions_file_paths,
                                                                  s.templates,
                                                                  s.prediction_categories,
                                                                  s.categorize_by_template,
                                                                  s.categorize_predictions,
                                                                  s.mask_index,  # TODO
                                                                  s.print_stats)
            # plot
            v.make_barplot(s.prediction_categories, template2group_name2props, task_name)

        if ANALYZE_LEFT_BIGRAM_FREQUENCY_PERCENTILES:

            # categorize productions into bi-gram percentile categories
            template2group_name2props = prepare_data_for_plotting(group2predictions_file_paths,
                                                                  s.templates,
                                                                  bigram_frequency_percentiles,
                                                                  s.categorize_by_template,
                                                                  categorize_left_bigrams,
                                                                  s.mask_index,  # TODO
                                                                  s.print_stats)

            # plot
            v.make_barplot(bigram_frequency_percentiles, template2group_name2props, task_name,
                           xlabel='left bi-gram frequency percentile')

        if ANALYZE_RIGHT_BIGRAM_FREQUENCY_PERCENTILES:

            # categorize productions into bi-gram percentile categories
            template2group_name2props = prepare_data_for_plotting(group2predictions_file_paths,
                                                                  s.templates,
                                                                  bigram_frequency_percentiles,
                                                                  s.categorize_by_template,
                                                                  categorize_right_bigrams,
                                                                  s.mask_index,  # TODO
                                                                  s.print_stats)

            # plot
            v.make_barplot(bigram_frequency_percentiles, template2group_name2props, task_name,
                           xlabel='right bi-gram frequency percentile')
