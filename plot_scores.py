import importlib

from babeval.visualizer import Visualizer


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
    v.make_barplot(s.prediction_categories, s.template2group_name2props, s.task_name)
