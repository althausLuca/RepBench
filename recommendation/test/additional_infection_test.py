import flaml
import numpy as np
import pandas as pd
from flaml.tune.analysis import ExperimentAnalysis

# load injected Dataset
from injection import inject_data_df
from injection.injection_config import AMPLITUDE_SHIFT, POINT_OUTLIER , DISTORTION
from repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator

# load injected Dataset
factors = [2, 5]
config_search_space = {
    "repair_truncation": flaml.tune.choice([2, 3, 4, 5]),
    "threshold": flaml.tune.loguniform(1.0, 3.0),
    "repair_iter": flaml.tune.choice([1, 10]),
    "n_max_iter": flaml.tune.choice([1, 20]),
    "classification_truncation": flaml.tune.choice([1, 2, 3, 4, 5]),
    "delta": flaml.tune.loguniform(1.5, 3.0),
}


for dataset in [ "elec" ]: # "bafu5k", , "elec"]:
    for a_type in [POINT_OUTLIER]:
        truth_df = pd.read_csv(f"data/test/{dataset}.csv")
        injected_df, _ = inject_data_df(truth_df, a_type=a_type)
        augmented_injected_df, anomaly_ranges = inject_data_df(injected_df, a_type=a_type , factor=factors[1])
        print(anomaly_ranges)

        def evaluate_config(config: dict):
            rmse = Robust_PCA_estimator(**config).scores(augmented_injected_df, injected_df, [1], None)["rmse"]
            return rmse



        def evaluate_config_augmented(config: dict):
            repair = Robust_PCA_estimator(**config).repair(augmented_injected_df, injected_df, [0], None)

            # rmse of the repaired data only on 80% of the non amomalos data
            diff = np.array(repair.iloc[:,[0]]-injected_df.iloc[:,[0]])
            # anomaly_ranges boolean array
            range_array = np.zeros_like(diff)
            for anomaly_range in anomaly_ranges:
                range_array[anomaly_range] = 1
            diff_anomalous = diff[range_array == 1]
            diff_non_anomalous = diff[range_array == 0]
            ## drop 20% of the non anomalous diff values with the highest difference
            diff_non_anomalous = diff_non_anomalous[np.argsort(diff_non_anomalous)[:-int(len(diff_non_anomalous)*0.2)]]

            rmse = np.sqrt(np.mean(np.square(np.concatenate((diff_anomalous, diff_non_anomalous)))))
            print(rmse)
            return rmse


        analysis: ExperimentAnalysis = flaml.tune.run(
            evaluate_config,  # the function to evaluate a config
            config=config_search_space,  # the search space defined
            mode="min",  # the optimization mode, "min" or "max"
            num_samples=500,  # the maximal number of configs to try, -1 means infinite
            time_budget_s=60,  # the time budget in seconds
            # use_ray=True,
        )


        analysis_augmented : ExperimentAnalysis = flaml.tune.run(
            evaluate_config_augmented,  # the function to evaluate a config
            config=config_search_space,  # the search space defined
            mode="min",  # the optimization mode, "min" or "max"
            num_samples=500,  # the maximal number of configs to try, -1 means infinite
            time_budget_s=60,  # the time budget in seconds
            # use_ray=True,
        )


        print(analysis.best_config,"non augmented")
        print(analysis_augmented.best_config,"augmented")

        print("augmented problem:")
        print(Robust_PCA_estimator(**analysis.best_config).scores(augmented_injected_df, injected_df, [0], None)["rmse"])
        print(Robust_PCA_estimator(**analysis_augmented.best_config).scores(augmented_injected_df, injected_df, [0], None)["rmse"])

        print("initial problem:")
        print(Robust_PCA_estimator(**analysis.best_config).scores(injected_df.copy(),truth_df.copy(),[0],None)["rmse"])
        print(Robust_PCA_estimator(**analysis_augmented.best_config).scores(injected_df.copy(), truth_df.copy(), [0], None)["rmse"])
        print("default")
        print(Robust_PCA_estimator().scores(injected_df.copy(), truth_df.copy(), [0], None)["rmse"])


