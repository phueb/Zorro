import importlib

from babeval.visualizer import Visualizer
from babeval.structure import prepare_data_for_barplot_open_ended, prepare_data_for_scatterplot
from babeval.bigrams import categorize_left_bigrams, categorize_right_bigrams
from babeval.bigrams import bigram_frequency_percentiles, bigram2f
from babeval.bigrams import w2max_left_bigram_f, w2max_right_bigram_f
from babeval.io import get_group2predictions_file_paths

# chose one
ANALYZE_PREDICTION_CATEGORIES = 1
ANALYZE_LEFT_BIGRAM_FREQUENCY_PERCENTILES = 0
ANALYZE_RIGHT_BIGRAM_FREQUENCY_PERCENTILES = 0
ANALYZE_MAX_VS_PREDICTED_LEFT_BIGRAM_FREQUENCY = 0
ANALYZE_MAX_VS_PREDICTED_RIGHT_BIGRAM_FREQUENCY = 0

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
    s = importlib.import_module(f'babeval.{task_name}.score_open_ended')

    for step in list(range(0, MAX_STEP + STEP_SIZE, STEP_SIZE)):

        # load prediction files
        group2predictions_file_paths = get_group2predictions_file_paths(task_name, 'open_ended', step)

        v = Visualizer(group2predictions_file_paths, step)

        if ANALYZE_PREDICTION_CATEGORIES:
            # categorize productions into production categories
            template2group_name2props = prepare_data_for_barplot_open_ended(group2predictions_file_paths,
                                                                            s.templates,
                                                                            s.prediction_categories,
                                                                            s.categorize_by_template,
                                                                            s.categorize_predictions,
                                                                            )
            # plot
            v.make_barplot(s.prediction_categories, template2group_name2props, task_name)

        if ANALYZE_LEFT_BIGRAM_FREQUENCY_PERCENTILES:
            # categorize productions into bi-gram percentile categories
            template2group_name2props = prepare_data_for_barplot_open_ended(group2predictions_file_paths,
                                                                            s.templates,
                                                                            bigram_frequency_percentiles,
                                                                            s.categorize_by_template,
                                                                            categorize_left_bigrams,
                                                                            )
            # plot
            v.make_barplot(bigram_frequency_percentiles, template2group_name2props, task_name,
                           xlabel='left bi-gram frequency percentile')

        if ANALYZE_RIGHT_BIGRAM_FREQUENCY_PERCENTILES:
            # categorize productions into bi-gram percentile categories
            template2group_name2props = prepare_data_for_barplot_open_ended(group2predictions_file_paths,
                                                                            s.templates,
                                                                            bigram_frequency_percentiles,
                                                                            s.categorize_by_template,
                                                                            categorize_right_bigrams,
                                                                            )
            # plot
            v.make_barplot(bigram_frequency_percentiles, template2group_name2props, task_name,
                           xlabel='right bi-gram frequency percentile')

        if ANALYZE_MAX_VS_PREDICTED_LEFT_BIGRAM_FREQUENCY:
            direction = "left"
            group2xy = prepare_data_for_scatterplot(group2predictions_file_paths,
                                                    w2max_left_bigram_f,
                                                    bigram2f,
                                                    direction
                                                    )
            # plot
            v.make_scatterplot(task_name,
                               group2xy,
                               xlabel=f'max {direction} bi-gram log-frequency',
                               ylabel=f'predicted {direction} bi-gram log-frequency',
                               )

        if ANALYZE_MAX_VS_PREDICTED_RIGHT_BIGRAM_FREQUENCY:
            direction = "right"
            group2xy = prepare_data_for_scatterplot(group2predictions_file_paths,
                                                    w2max_right_bigram_f,
                                                    bigram2f,
                                                    direction
                                                    )
            # plot
            v.make_scatterplot(task_name,
                               group2xy,
                               xlabel=f'max {direction} bi-gram log-frequency',
                               ylabel=f'predicted {direction} bi-gram log-frequency',
                               )
