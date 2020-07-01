from babeval import configs


def get_group2predictions_file_paths(task_name):
    # get prediction file paths from this repository (dummies)
    if configs.Eval.dummy:
        group2pattern = {g: f'probing_{task_name}_results_{configs.Eval.step}_{g}*.txt'
                         for g in ['dummy0', 'dummy1']}
        group2predictions_file_paths = {g: [p for p in configs.Dirs.dummy_predictions.glob(pattern)]
                                        for g, pattern in group2pattern.items()}

    # get prediction file paths from lab server
    else:
        group2pattern = {g: f'{g}/**/saves/probing_{task_name}_results_{configs.Eval.step}.txt'
                         for g in configs.Eval.param_names}
        print(group2pattern)
        group2predictions_file_paths = {g: [p for p in configs.Dirs.predictions.rglob(pattern)][:configs.Eval.max_reps]
                                        for g, pattern in group2pattern.items()}

    # check paths
    for k, v in group2predictions_file_paths.items():
        assert v, f'Did not find prediction files for group ={k}'
        print(k)
        print(v)

    return group2predictions_file_paths
