from matplotlib import pyplot as plt

from Injection.Scenarios.scen_gen import build_scenario
from Injection.injected_data_container import InjectedDataContainer
from RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
import matplotlib

from repair import CDRecEstimator

matplotlib.use('TKAgg')

import ast

scen_name = "a_size"
anomaly_type = "shift"
data_name = "bafu"
Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="train", cols=[0])

rpa = Robust_PCA_estimator(n_max_iter=50)
part_scen: InjectedDataContainer
for part_name, part_scen in Scenario.part_scenarios.items():
    injected_columns = part_scen.repair_inputs["columns_to_repair"]
    truth , injected = part_scen.repair_inputs["truth"].iloc[:,injected_columns] , part_scen.repair_inputs["injected"].iloc[:,injected_columns]
    scores = rpa.scores(**part_scen.repair_inputs)
    repair  = rpa.repair(**part_scen.repair_inputs)

    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


print("------one reduction ------------")
rpa = Robust_PCA_estimator(n_max_iter=0)
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print("------one reduction no normalization ------------")
rpa = Robust_PCA_estimator(n_max_iter=0)
rpa.normalize_before = False

for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


print("------CD reduction ------------")
import time
rpa = CDRecEstimator(n_max_iter=20)
start = time.time()
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print(time.time()-start)
print("------one reduction ------------")
rpa = CDRecEstimator(n_max_iter=0)

start = time.time()
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print(time.time()-start)


print(time.time()-start)
print("------one reduction no normalization ------------")
rpa = CDRecEstimator(n_max_iter=0)
rpa.normalize_before = False
start = time.time()
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print(time.time()-start)
