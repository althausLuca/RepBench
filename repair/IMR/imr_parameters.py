from testing_frame_work.scenarios.scen_generator import build_scenario
from injection.injectedDataContainer import InjectedDataContainer
from repair.IMR.IMR_estimator import IMR_estimator
import matplotlib

matplotlib.use('TKAgg')

scen_name = "a_factor"
anomaly_type = "shift"
data_name = "bafu"
Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="train", cols=[0])

rpa = IMR_estimator(tau=0.1)
part_scen: InjectedDataContainer
for part_name, part_scen in Scenario.part_scenarios.items():
    injected_columns = part_scen.repair_inputs["columns_to_repair"]
    truth , injected = part_scen.repair_inputs["truth"].iloc[:,injected_columns] , part_scen.repair_inputs["injected"].iloc[:,injected_columns]
    scores = rpa.scores(**part_scen.repair_inputs)
    repair  = rpa.repair(**part_scen.repair_inputs)

    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


print("------one reduction ------------")
rpa = IMR_estimator(tau=0.01)
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print("------one reduction no normalization ------------")
rpa = IMR_estimator(tau=0.001)
rpa.normalize_before = False

for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


