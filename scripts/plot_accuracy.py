import importlib
from collections import defaultdict
import numpy as np
import yaml
from pathlib import Path

from zorro import configs
from zorro.prepare import prepare_data_for_plotting
from zorro.io import get_group2predictions_file_paths
from zorro.figs import show_barplot
from zorro.visualizer import Visualizer, ParadigmData

SHOW_BAR_PLOTS = False

PARADIGMS = [
    # irregular forms
    'irregular_verb_passive',
    'irregular_verb_intransitive',
    'irregular_verb_transitive',
    # agreement
    'agreement_in_1_verb_question',
    'agreement_in_2_verb_question',
    'agreement_across_1_adjective',
    'agreement_across_2_adjectives',
    'agreement_across_PP',
    'agreement_across_RC',
    'agreement_between_neighbors',
]

# where to get files from?
if configs.Eval.local_runs:
    runs_path = configs.Dirs.runs_local
else:
    runs_path = configs.Dirs.runs_remote


def filter_by_step(prediction_file_path: Path,
                   step: int,
                   ) -> bool:
    if int(prediction_file_path.stem.split('_')[-1]) == step:
        return True

    return False


# collects and plots each ParadigmData instance in 1 multi-axis figure
v = Visualizer(num_paradigms=len(PARADIGMS))

for paradigm in PARADIGMS:
    # load module
    s = importlib.import_module(f'zorro.{paradigm}.score')

    # group_names
    if configs.Eval.param_names is None:
        group_names_ = sorted([p.name for p in runs_path.glob('*')])
    else:
        group_names_ = configs.Eval.param_names

    # filter group_names
    if configs.Eval.included_params:
        group_names = []
        for group_name in group_names_:
            path = runs_path / group_name / 'param2val.yaml'
            with path.open('r') as f:
                param2val = yaml.load(f, Loader=yaml.FullLoader)
            for k, v in configs.Eval.included_params.items():
                if param2val[k] == v:
                    group_names.append(group_name)
    else:
        group_names = group_names_

    print(f'Found params={group_names}')

    # load prediction files at all available steps
    print('Loading model prediction files...')
    group2predictions_file_paths = get_group2predictions_file_paths(group_names,
                                                                    runs_path,
                                                                    paradigm,
                                                                    )

    # init line plot data
    pd = ParadigmData(name=paradigm,
                      group_name2template2curve=defaultdict(dict),
                      group_names=group_names + configs.Data.control_names,
                      group2prediction_file_paths=group2predictions_file_paths
                      )

    for step in configs.Eval.steps:

        # filter files by step
        group2predictions_file_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                                for g, fps in group2predictions_file_paths.items()}

        # calc + collect accuracy
        template2group_name2props = prepare_data_for_plotting(group2predictions_file_paths_at_step,
                                                              paradigm,
                                                              s.templates,
                                                              s.categorize_by_template,
                                                              s.grammar_checker,
                                                              )

        # plot accuracy comparison at current time step
        if SHOW_BAR_PLOTS:
            show_barplot(template2group_name2props,
                         group2predictions_file_paths,
                         paradigm,
                         step,
                         verbose=True,
                         )

        # collect data for paradigm
        for template, group_name2props in template2group_name2props.items():
            for group_name, props in group_name2props.items():
                curve_i = np.mean(props)  # the mean proportion of a group at one location on curve
                pd.group_name2template2curve[group_name].setdefault(template, []).append(curve_i)

    # plot each paradigm in separate axis
    v.update(pd)

v.plot_summary()
v.plot_with_legend()
