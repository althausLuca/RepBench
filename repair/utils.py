import repair as algs
import repair.algorithms_config as ac
import toml

"""
Mapping of algorithm names to the actual estimator classes (used when ever we need to create an estimator object)
make sure to include the estimator in the repair.__init__.py file 
"""
algo_mapper = {
    ac.RPCA: algs.Robust_PCA_estimator,
    ac.SCREEN: algs.SCREENEstimator,
    ac.IMR: algs.IMR_estimator,
    ac.CDREP: algs.CDRecEstimator,
    ac.SPEEDandAcceleration: algs.SpeedAndAccelerationEstimator,
    ac.SCR: algs.SCREstimator,
    ac.KalmanFilter : algs.KalmanFilterEstimator,
}

alias_mapper = {}
aliases = ac.AlgorithmAliases
for alg_name,estimator in algo_mapper.items():
    for alias in aliases[alg_name]:
        alias_mapper[alias] = estimator
algo_mapper.update(alias_mapper)

def get_main_alg_name(name : str):
    main_names = ac.ALGORITHM_TYPES
    if name in main_names:
        return name
    else:
        for main_name, aliases_ in ac.AlgorithmAliases.items():
            if name in aliases_:
                return main_name
        raise ValueError(f'Unknown algorithm name: {name} must be one from {alias_mapper.keys()}')


def get_algorithm_params(alg_name):
    with open('repair/parameters.toml', 'r') as f:
        params = toml.load(f)

    if alg_name in params:
        return params[alg_name]
    else:
        raise ValueError(f'Unknown algorithm name: {alg_name} must be one from {params.keys()}')
