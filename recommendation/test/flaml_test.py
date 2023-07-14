import flaml
import pandas as pd
from flaml import AutoML
from flaml.tune.analysis import ExperimentAnalysis

# load injected Dataset
from injection import inject_data_df
from injection.injection_config import AMPLITUDE_SHIFT, POINT_OUTLIER, DISTORTION
from repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator
from repair.algorithms_config import IMR, SCREEN, RPCA, CDREP
from repair.algorithm_mapper import algo_mapper

# load injected Dataset

dimensionality_decomposition_search_space = {
    "repair_truncation": flaml.tune.choice([2, 3, 4, 5]),
    "threshold": flaml.tune.loguniform(1.0, 3.0),
    "repair_iter": flaml.tune.choice([1, 10]),
    "n_max_iter": flaml.tune.choice([1, 20]),
    "classification_truncation": flaml.tune.choice([1, 2, 3, 4, 5]),
    "delta": flaml.tune.loguniform(1.5, 3.0),
}

screen_search_space = {
    "smin": flaml.tune.uniform(-2, -0.025),
    "smax": flaml.tune.loguniform(0.025, 2),
}

imr_search_space = {
    "p": flaml.tune.choice([1, 3, 5, 10, 15]),
    "tau": flaml.tune.loguniform(0.01, 0.9),
}

config_map = {IMR: imr_search_space,
              SCREEN: screen_search_space,
              RPCA: dimensionality_decomposition_search_space,
              CDREP: dimensionality_decomposition_search_space
              }



def flaml_search(data_set, a_type, factor=2):
    truth_df = pd.read_csv(f"data/test/{dataset}.csv")
    injected_df, _ = inject_data_df(truth_df, a_type=a_type)

    tasks = [
        # {
        #     "task_id": "IMR",
        #     "custom_fun": lambda config: algo_mapper[IMR](**config).score(injected_df, truth_df, [0], None)["rnse"],
        #     "search_space": config_map[IMR],
        #     'time_budget': 60,  # in seconds
        #     'early_stop': 10,
        # },
        {
            "task_id": "SCREEN",
            "custom_fun": lambda config: algo_mapper[SCREEN](**config).score(injected_df, truth_df, [0], None)["rnse"],
            "search_space": config_map[SCREEN],
            'time_budget': 60,  # in seconds
            'early_stop': 10,
        },
        {
            "task_id": "RPCA",
            "custom_fun": lambda config: algo_mapper[RPCA](**config).score(injected_df, truth_df, [0], None)["rnse"],
            "search_space": config_map[RPCA],
            'time_budget': 60,  # in seconds
            'early_stop': 10,
        },
        {
            "task_id": "CDREC",
            "custom_fun": lambda config: algo_mapper[CDREP](**config).score(injected_df, truth_df, [0], None)["rnse"],
            "search_space": config_map[CDREP],
            'time_budget': 60,  # in seconds
            'early_stop': 10,
        },
    ]

    automl = AutoML()
    automl_settings = {
        'time_budget': 1800,  # in seconds
        'metric': 'minimize',
        'log_file_name': 'flaml.log',
        'seed': 42
    }
    best_config, best_task_id = automl.fit(tasks, **automl_settings)

    # label    print(f"Best hyperparameters for task {best_task_id}: {best_config}")
    print(f"Output value for task {best_task_id}: {automl.get_best_result()}")


for dataset in ["bafu5k", "humidity", "elec"]:
    for a_type in [AMPLITUDE_SHIFT, POINT_OUTLIER, DISTORTION]:
        flaml_search(dataset, a_type)
        # truth_df = pd.read_csv(f"data/test/{dataset}.csv")
        #
        # injected_df, _ = inject_data_df(truth_df, a_type=a_type)
        #
        # #
        # #
        # import time
        #
        # start = time.time()
        # analysis: ExperimentAnalysis = flaml.tune.run(
        #     evaluate_config,  # the function to evaluate a config
        #     config=config_search_space,  # the search space defined
        #     mode="min",  # the optimization mode, "min" or "max"
        #     num_samples=500,  # the maximal number of configs to try, -1 means infinite
        #     time_budget_s=60,  # the time budget in seconds
        #     # use_ray=True,
        # )
        # flaml_time = time.time() - start
        #
        # b_opt_search_space = Robust_PCA_estimator().suggest_param_range(injected_df)
        #
        # print("Start Bayesian Optimization")
        # from algorithms.parameterization import BayesianOptimizer
        #
        # ## do the same with the BayesianOptimizer
        # bo = BayesianOptimizer(estim=Robust_PCA_estimator(), error_score="rmse")
        #
        # start = time.time()
        # bo_params, _, score = bo.find_optimal_params(
        #     {"injected": injected_df, "truth": truth_df, "columns_to_repair": [0]}, b_opt_search_space)
        # bo_time = time.time() - start
        #
        # print("dataset", dataset, "a_type", a_type)
        # print("Bo", bo_params)
        # print("flaml", analysis.best_config)
        #
        # print("Bo_score", score)
        # print("flaml_score", analysis.best_result)
        # print("Bo_time", bo_time, time)
        # print("flaml_time", flaml_time)
        #
        # # save all the above prints to a csv file named with the dataset and anomaly type
        # import csv
        #
        # filename = f"FlamlVSBo{dataset}_{a_type}.csv"
        #
        # with open(filename, mode='w', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     # writer.writerow(["dataset", "a_type", "Bo", "flaml", "Bo_score", "flaml_score", "Bo_time", "flaml_time"])
        #     writer.writerow(["flaml_params", "flaml_score"])
        #     print(analysis.best_config, analysis.best_result["_metric"])
        #     print(analysis.best_config, analysis.best_result)
        #     writer.writerow([analysis.best_config, analysis.best_result["_metric"]])
        #     writer.writerow(["Bo_params", "Bo_score"])
        #     writer.writerow([bo_params, score])
        #     # writer.writerow([dataset, a_type, bo_params, analysis.best_config, score, analysis.best_result, bo_time, flaml_time])
        #
        # print("Results saved to", filename)
