import numpy as np
import pandas as pd


from repair.IMR.IMR_estimator import IMR_estimator
from repair.Screen.screen_estimator import SCREENEstimator
from repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import Injection.Scenarios.ScenarioConfig as sc
import testing_frame_work.repair as repair_r
sc.MAX_N_ROWS = 5000

plt.figure(figsize=(25, 6), dpi=80)

scen_name = "base"

dataset_names = ["bafu5k.csv", "msd1_5.csv", "elec.csv", "humidity.csv"]
a_types = ["shift", "outlier", "distortion"]


error_metrics = ["full_rmse", "partial_rmse", "mae"]

param_list_dict = {"imr": [{"p": 1, "tau": tau} for tau in np.linspace(0, 0.5, 100)][1:],
                   "screen" : [{"smin": -s, "smax": s} for s in np.linspace(0, 2, 100)[2:]],
                   "rpca" : [{"threshold": t, "classification_truncation": 2} for t in np.linspace(0, 3, 100)[1:]]
                   }

main_param_dict = {"imr": "tau" , "screen" : "smax" , "rpca" : "threshold" } #"classification_truncation"}
estimator_dict = {"imr": IMR_estimator, "screen" : SCREENEstimator , "rpca" : Robust_PCA_estimator }


pdf = matplotlib.backends.backend_pdf.PdfPages(f"anomaly_plots.pdf")

def min_max(vec):
    return vec
    min_ = min(vec)
    max_ = max(vec)
    if min_ == max_:
        return vec
    diff = max_ - min_
    return [(v - min_) / diff for v in vec]



for dataset_name in dataset_names:
    for error in error_metrics:
        bars = {}
        for ax_index, a_type in enumerate(a_types):
            bars[a_type] = {}

            scen = Scenario(scen_name=scen_name, data=dataset_name, a_type=a_type)
            for name, part_scen in scen.part_scenarios.items():
                train_part: DataPart = part_scen.train
                repair_inputs = train_part.repair_inputs
                oringinal_rmse = train_part.original_scores[error]

            for alg_type in ["imr" , "screen"]:
                score = repair_r.run_repair(alg_type , **repair_inputs)["scores"][error]
                bars[a_type][alg_type] = score
        pd.DataFrame(bars).plot(kind='bar')
        plt.title(error)
        pdf.savefig(plt.gcf())
        plt.show()

pdf.close()
