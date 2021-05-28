"""
compare end-of-training accuracy between models that vary in:
1. framework: huggingface vs. fairseq
2. implementation: official vs. custom code
3. architecture: roBERTa-base vs. BabyBERTa
4: configuration: parameters, e.g. corpus
"""

from zorro import configs
from zorro.figs import show_barplot
from zorro.utils import prepare_data_for_plotting, get_phenomena_and_paradigms
from zorro.io import get_group2model_output_paths

# where to get files from?
runs_path = configs.Dirs.runs_local
configs.Eval.local_runs = True

group_names = sorted([p.name for p in runs_path.glob('*')])
print(f'Found {group_names}')

# for all paradigms
for phenomenon, paradigm in get_phenomena_and_paradigms():

    # load model output at all available steps
    group2model_output_paths = get_group2model_output_paths(group_names,
                                                            runs_path,
                                                            phenomenon,
                                                            paradigm,
                                                            )

    # calc + collect accuracy
    template2group_name2accuracies = prepare_data_for_plotting(group2model_output_paths,
                                                               phenomenon,
                                                               paradigm,
                                                               )

    # plot accuracy comparison at current time step
    show_barplot(template2group_name2accuracies,
                 group2model_output_paths,
                 paradigm,
                 step='end-of-training',
                 verbose=True,
                 conditions=['is_official', 'is_base', 'is_reference', 'framework']
                 )
