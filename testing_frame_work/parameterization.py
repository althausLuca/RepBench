from repair import algo_mapper
from repair.parameterization.optimizers.estimator_optimizer import EstimatorOptimizer
from repair.parameterization.optimizers.succesivehalving_search import SuccessiveHalvingOptimizer
from repair.parameterization.optimizers.bayesian_optimization import BayesianOptimizer
import toml


### Parameters from toml file
file_name = "repair/parameters.toml"
def load_params_from_toml(alg_type):
    param_dict = toml.load(file_name)
    assert alg_type in param_dict or alg_type.split("_")[0] in param_dict , f"{alg_type} not in {param_dict.keys()}"
    if alg_type in param_dict:
        return param_dict[alg_type]
    return param_dict[alg_type.split("_")[0]]



optim_methods = {"grid": EstimatorOptimizer,
                "halving": SuccessiveHalvingOptimizer,
                "bayesian": BayesianOptimizer}

# def params_from_training_set(scen_name,anomaly_type,data_name,train_method,train_metric,train_part,repair_type):
#     store_name = f"{scen_name}_{anomaly_type}_{data_name}_{train_method}_{train_metric}"
#     train_hash = train_part.hash(train_method + train_metric)
#     try:
#         # check if params are already computed for this dataset and eror
#         params, runtime = load_train(repair_type, store_name, id=train_hash)
#         raise NotImplementedError
#     except:
#         params, train_time = find_params(repair_type, metric=train_metric, train_method=train_method,
#                                                     repair_inputs=train_part.repair_inputs, store=store_name, id=train_hash)
#     return params
#
# def find_params(alg_type, metric, train_method,repair_inputs , store = False , id =None):
#     estimator = algo_mapper[alg_type]
#
#     print("training", alg_type)
#     print("train size:", repair_inputs["injected"].shape)
#
#     param_grid = estimator.suggest_param_range(repair_inputs["injected"])
#     estimator_optimizer = optim_methods[train_method](estimator, metric)
#
#     optimal_params , search_time = estimator_optimizer.find_optimal_params(repair_inputs, param_grid)
#
#     if store:
#         assert isinstance(store,str)
#         save_train(alg_type,store,optimal_params,id =id)
#     return optimal_params, search_time
#
#
#
# def save_train(alg_type,name, params , id = None):
#     if id is None:
#         id = name
#
#     path = f"TrainResults/{alg_type}"
#     file_name = "train_results.toml"
#
#     try:
#         toml_dict = toml.load(f'{path}/{file_name}')
#     except :
#         toml_dict = {}
#         from pathlib import Path
#         Path(path).mkdir(parents=True, exist_ok=True)
#
#     params["names"] = [name]
#     toml_dict[id] = params
#
#     with open(f'{path}/{file_name}', 'w') as f:
#         print(toml_dict)
#         toml.dump(toml_dict, f, encoder=toml.TomlNumpyEncoder(preserve=True))

# def load_train(alg_type, name , id =None):
#     """
#     Raises exceptions if parameters can not be found
#
#     Parameters
#     ----------
#     alg_type : str
#     name : str
#
#     Returns : parametrs
#     -------
#     """
#
#     if id is None:
#         id = name
#
#     path = f"TrainResults/{alg_type}"
#     file_name = "train_results.toml"
#
#     toml_dict = toml.load(f'{path}/{file_name}')
#     params = toml_dict[id]
#
#     current_names = params.get("names",[])
#
#     if name not in current_names:
#         params["names"] = current_names + [name]
#         with open(f'{path}/{file_name}', 'w') as f:
#             toml.dump(toml_dict, f, encoder=toml.TomlNumpyEncoder(preserve=True))
#
#     del params["names"]
#
#     return params


