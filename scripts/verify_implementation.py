"""
compare end-of-training accuracy between models that vary in:
1. framework: huggingface vs. fairseq
2. implementation: official vs. custom code
3. architecture: roBERTa-base vs. BabyBERTa
4: configuration: parameters, e.g. corpus,
"""

from zorro import configs
from zorro.figs import show_barplot
from zorro.prepare import prepare_data_for_plotting

conditions = ['framework', 'is_official', 'is_base', 'is_reference' ]


phenomena = [
    'npi_licensing',
    'ellipsis',
    'filler-gap',
    'case',
    'argument_structure',
    'local_attractor',
    'agreement_subject_verb',
    'agreement_demonstrative_subject',
    'irregular_verb',
    'island-effects',
    'quantifiers',
]

EXCLUDED_PARADIGMS = [
    'existential_there_2',  # too difficult
    'across_2_adjectives',  # very similar performance to across_1_adjective
]

# where to get files from?
if configs.Eval.local_runs:
    runs_path = configs.Dirs.runs_local
else:
    runs_path = configs.Dirs.runs_remote


# get list of (phenomenon, paradigm) tuples
phenomena_paradigms = []
for phenomenon in phenomena:
    for p in (configs.Dirs.src / phenomenon).glob('*.py'):
        paradigm = p.stem
        if paradigm in EXCLUDED_PARADIGMS:
            continue
        phenomena_paradigms.append((phenomenon, paradigm))


# for all paradigms
for phenomenon, paradigm in phenomena_paradigms:

    # load model output at all available steps
    group2model_output_paths = get_group2model_output_paths(group_names,
                                                            runs_path,
                                                            phenomenon,
                                                            paradigm,
                                                            )


    # filter files by step
    group2model_output_paths_at_step = {g: [fp for fp in fps if filter_by_step(fp, step)]
                                        for g, fps in group2model_output_paths.items()}

    # calc + collect accuracy
    template2group_name2accuracies = prepare_data_for_plotting(group2model_output_paths_at_step,
                                                               phenomenon,
                                                               paradigm,
                                                               )

    # plot accuracy comparison at current time step
    show_barplot(template2group_name2accuracies,
                 group2model_output_paths,
                 paradigm,
                 step='end-of-training',
                 verbose=True,
                 )