import json
import matplotlib.pyplot as plt
import os
import sys

from RepBenchWeb.BenchmarkMaps.repairCreation import create_injected_container

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..','..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.feature_extraction.load_features import load_data
from repair import Robust_PCA_estimator
from repair.parameterization import BayesianOptimizer

filename = "recommendation/test/scores.txt"
load_string = "injection_parameters"

with open(filename, "r") as f:
    lines = f.readlines()

score_results = [json.loads(line) for line in lines]


rpca_estimator = Robust_PCA_estimator()
optimizer = BayesianOptimizer(rpca_estimator,"rmse",n_initial_points=20)


for result in score_results:
    injection_parameters = result["injection_parameters"]

    rpca_parameters = result["alg_results"]["rpca"]["parameters"]


    injected_df , truth_df = load_data(injection_parameters, return_truth=True)
    injected_df_col = injected_df.iloc[:, injection_parameters["cols"]]
    truth_df_col = truth_df.iloc[:, injection_parameters["cols"]]

    search_space = rpca_estimator.suggest_param_range(injected_df)
    repair_inputs = {"injected":injected_df,"truth":truth_df,"columns_to_repair":injection_parameters["cols"]}






    ## old way score
    injected_data_container = create_injected_container(injected_df=injected_df,truth_df=truth_df)

    print("SCORE AS IN RETRIVAL METHOD", Robust_PCA_estimator(**rpca_parameters).scores(**injected_data_container.repair_inputs))



    params, time , score = optimizer.find_optimal_params(repair_inputs,search_space)
    print("optparams" , params)
    print("score after opt" , score)
    print("refitted opt optscore" , Robust_PCA_estimator(**params).scores(**repair_inputs))

    # refitted opt optscore
    # {'mae': 0.009472824890808813, 'rmse': 0.09307174523487464, 'partial_rmse': 0.0,
    #  'rmse_per_col': [(7, 0.09307174523487464)], 'original_rmse': 0.0991849261098699}

    #
    # plt.plot(injected_df_col,label="injected")
    # plt.plot(truth_df_col,label="truth")
    # plt.legend()
    # plt.show()

