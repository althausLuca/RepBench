from injection.injection import  load_injected_container
from repair.algorithm_mapper import algo_mapper
from repair.algorithms_config import CDREP, SCREEN ,RPCA
from repair.parameterization import (
    BayesianOptimizer,
    SuccessiveHalvingOptimizer,
    EstimatorOptimizer as GridSearchOptimizer)
from repair import Estimator


injection_parameters = {"seed": 100,
                        "factor": 2,
                        "cols": [0],
                        "dataset": "bafu200.csv",
                        "a_type": "shift",
                        "a_percent": 14}



injectedDataContainer = load_injected_container(injection_parameters,"data/train")
alg_name = RPCA
alg : Estimator = algo_mapper[alg_name]()

param_grid = alg.suggest_param_range(injectedDataContainer.injected)
param_grid = {"classification_truncation" : param_grid["classification_truncation"], "threshold" : param_grid["threshold"] }

bayes_opt = BayesianOptimizer(alg,"rmse")

params,time,score = bayes_opt.find_optimal_params(injectedDataContainer.repair_inputs,param_grid)
print("optimal parameters:" , params, "time:",time, "score:", score)
