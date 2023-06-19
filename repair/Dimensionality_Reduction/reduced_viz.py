import pandas as pd
from matplotlib import pyplot as plt

from Injection.Scenarios.scen_gen import build_scenario
from Injection.injected_data_container import InjectedDataContainer
from RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
import matplotlib

from repair import CDRecEstimator

matplotlib.use('TKAgg')

import ast

scen_name = "a_factor"
anomaly_type = "outlier"
data_name = "humidity"
Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="train", cols=[0])

part_scen: InjectedDataContainer
part_name, part_scen = list(Scenario.part_scenarios.items())[5]
print(part_name)

cols_to_repair = part_scen.repair_inputs["columns_to_repair"]


for i,delta in enumerate([1.2]):#0.5, 1, 1.2, 2]):
    rpca = CDRecEstimator(delta=delta,n_max_iter=10)
    rpca.repair(**part_scen.repair_inputs)
    print(rpca.weights_i_)
    print(rpca.reduced_i_)
columns_to_repair = part_scen.repair_inputs["columns_to_repair"]
plt.plot(part_scen.repair_inputs["injected"].iloc[:,columns_to_repair],color= "yellow",label="injected")
plt.plot(part_scen.repair_inputs["truth"].iloc[:,columns_to_repair] , color="black",label="truth")

pd.DataFrame()
for (k,v) in list(rpca.reduced_i_["classify"].items())[::2]:
    plt.plot(v[:,columns_to_repair[0]],label=k)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/reduced.pdf',bbox_inches='tight')
plt.clf()

for (k,v) in list(rpca.weights_i_["classify"].items())[::2]:
    plt.plot(v,label=k)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/weights.pdf',bbox_inches='tight')
plt.clf()

pd.DataFrame(rpca.weights_i_["classify"]).iloc[:200,:].to_csv(f'algorithms/Dimensionality_Reduction/weight_results/weights.csv')
reduced_csv = pd.DataFrame({k:v[:,columns_to_repair[0]] for k,v in  rpca.reduced_i_["classify"].items()})
reduced_csv["truth"] = part_scen.repair_inputs["truth"].iloc[:,columns_to_repair]
reduced_csv["injected"] =part_scen.repair_inputs["injected"].iloc[:,columns_to_repair]
reduced_csv.iloc[:200,:].to_csv(f'algorithms/Dimensionality_Reduction/weight_results/reduced.csv',index_label="t")
