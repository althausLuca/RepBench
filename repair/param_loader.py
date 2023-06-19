import toml


def get_algorithm_params(alg_name):
    with open('repair/parameters.toml', 'r') as f:
        params = toml.load(f)

    if alg_name in params:
        return params[alg_name]
    else:
        raise ValueError(f'Unknown algorithm name: {alg_name}')
