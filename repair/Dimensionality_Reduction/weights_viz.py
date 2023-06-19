import pandas as pd
from matplotlib import pyplot as plt

from Injection.Scenarios.scen_gen import build_scenario
from Injection.injected_data_container import InjectedDataContainer
from RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
import matplotlib

matplotlib.use('TKAgg')

scen_name = "a_factor"
anomaly_type = "outlier"
data_name = "bafu"
Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="train", cols=[1])

part_scen: InjectedDataContainer
part_name, part_scen = list(Scenario.part_scenarios.items())[2]
print(part_name)

columns_to_repair = part_scen.repair_inputs["columns_to_repair"]

result_df = pd.DataFrame({"injected" : part_scen.repair_inputs["injected"].iloc[:, columns_to_repair[0]].values,
                          "truth" : part_scen.repair_inputs["truth"].iloc[:, columns_to_repair[0]].values})

print(part_scen.repair_inputs["truth"].iloc[:, columns_to_repair])
print(result_df)
for i, delta in enumerate([[1, 1.2,2,500000000000][0]]):  # ]):
    rpca = Robust_PCA_estimator(delta=delta, n_max_iter=10,classification_truncation=3)
    rpca.repair(**part_scen.repair_inputs)
    for k,w_vec in enumerate(rpca.weights_i_["classify"].values()):
        result_df[f"delta_{delta}_iter_{k}"] = w_vec
    print(list(rpca.reduced_i_["classify"].values())[-2])
    result_df["reduced"] = rpca.reduced_i_["classify"][2][:,columns_to_repair[0]]
    print(result_df["reduced"])
result_df.round(3).iloc[800:1200, :].to_csv(f'algorithms/Dimensionality_Reduction/weight_results/deltaweights.csv', index_label="t")
result_df.round(3).iloc[800:1200, :].plot(style={'injected': 'r',"reduced":"black"})
plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/weightsdelta.pdf', bbox_inches='tight')
