import itertools
import pandas as pd
import numpy as np
import json
import os
import sys

from recommendation.utils.file_parsers import read_file_to_pandas

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from recommendation.feature_extraction.load_features import get_injection_parameter_hashes_checker


from repair import get_algorithm_params
import  injection.injection_config as inject_conf
from repair import algo_mapper
import  repair.algorithms_config as alg_conf
from datetime import datetime
from injection.injection import load_injected_data , create_injected_container


mode = "train"

# Get current date and time
now = datetime.now().strftime("%m-%d %H:%M:%S")

output_filename = f"recommendation/results/scores/results_{mode}"
log_file = f"recommendation/logs/{now}_ {mode}_logs"
data_folder = f"data/recommendation/{mode}"
datasets = os.listdir(data_folder)

factors = [2, 5, 10]
a_percentages = [4,5, 7, 11, 20]
col_n_cap = 8

score = alg_conf.RMSE
alg_names = alg_conf.ALGORITHM_TYPES
a_types = inject_conf.ANOMALY_TYPES


def append_to_file(data, filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('')

    with open(filename, 'a') as f:
        if isinstance(data, dict):
            f.write(json.dumps(data) + '\n')
        else:
            f.write(data + '\n')


injected_dfs = []
already_computed_checker = get_injection_parameter_hashes_checker(output_filename)

data_sets_to_col_n = {}
for dataset in datasets:
    truth_df: pd.DataFrame = read_file_to_pandas(f"{data_folder}/{dataset}")
    ts_cols = [[i] for i in range(min(truth_df.shape[1], col_n_cap))]
    data_sets_to_col_n[dataset] = truth_df.shape[1]

for columns, a_percentage, factor, a_type, dataset in itertools.product([ [0], [1], [2], [3]], a_percentages, factors,
                                                                        a_types, datasets):
    for c in columns:
        if c >= data_sets_to_col_n[dataset]:
            continue

    seed = 100
    np.random.seed(seed)
    injection_parameters = {
        "seed": seed,
        "factor": factor,
        "cols": columns,
        "dataset": dataset,
        "a_type": a_type,
        "a_percent": a_percentage
    }

    alg_name: str = "no algorithms yet"

    try:
        if already_computed_checker(injection_parameters):
            print("Already computed")
            continue
        injected_df, truth_df = load_injected_data(injection_parameters,data_folder=data_folder)



        injected_data_container = create_injected_container(injected_df=injected_df, truth_df=truth_df)
        injected_dfs.append(injected_df)
        injected_data_container.plot()
        alg_results = {}
        for alg_name in alg_names:
            alg_constructor = algo_mapper[alg_name]
            alg_results[alg_name] = {}

            parameters = get_algorithm_params(alg_name)
            alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs)[score]
            alg_results[alg_name] = {score: alg_score, "parameters": parameters}

        original_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs)[
            "original_rmse"]


        results = {"original rmse": original_score, "alg_results": alg_results,
                   "injection_parameters": injection_parameters}
        append_to_file(results, output_filename)

    except Exception as e:
        raise e
        import traceback

        print("Exception", e)
        print("failed to compute", alg_name,
              "with", injection_parameters,
              "with exception", e,
              "of type", type(e).__name__, traceback.format_exc())
        injection_parameters["alg"] = alg_name
        injection_parameters["exception"] = traceback.format_exc()
        injection_parameters["exception_type"] = type(e).__name__
        append_to_file(injection_parameters, log_file)
