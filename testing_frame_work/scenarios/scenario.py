import os

import numpy as np
import pandas as pd
import injection.injection_config as ac
from injection.injectedDataContainer import InjectedDataContainer
from testing_frame_work.scenarios import scenario_config as sc
from testing_frame_work.scenarios.scenario_saver.Scenario_saver import save_precision


class Scenario:
    def __init__(self, scen_name , data , a_type , data_container):
        assert a_type in ac.ANOMALY_TYPES
        self.a_type = a_type
        self.scen_name  = scen_name
        self.data_name = data.split(".")[0]
        self.part_scenarios = {}
        self.data_container = data_container

    def add_part_scenario(self,data_part, part_key):
        self.part_scenarios[part_key] = data_part

    @property
    def name_container_iter(self):
        return iter( [ (name , scen_part ) for name, scen_part in self.part_scenarios.items()])

    def get_amount_of_part_scenarios(self):
        return len(self.part_scenarios)


    @property
    def repair_names(self):
        return set(sum([p.repair_names for k,p in self.part_scenarios.items()],[]))

    @property
    def common_truth(self):
        if self.get_amount_of_part_scenarios() == 1:
            return True
        first_scen : InjectedDataContainer
        first_scen , *following_scen =  self.part_scenarios.values()
        return all([first_scen.truth.equals(other.truth) for other in following_scen])


    def score_dfs(self):
        used_scores = []
        full_dict = {}
        for part_name, part in self.part_scenarios.items():
            full_dict[part_name] = {}
            for (alg_name, alg_type) , scores in part.repair_metrics.items():
                full_dict[part_name][(alg_name,alg_type)] = scores
                used_scores += list(scores.keys())

        full_df = pd.DataFrame.from_dict(full_dict,orient="index")
        full_df.index.name = self.scen_name
        retval = {score : full_df.applymap(lambda x: x.get(score,np.NAN)) for score in set(scores)}
        return retval

    def save(self,*, plot_data=False,plot_repairs=False,res_name=None):
        save_folder = f"{sc.SAVE_FOLDER}"
        scenario_name = self.scen_name
        data_name = self.data_name
        anomaly_type = self.a_type

        if res_name is not None:
            path = f"{save_folder}/{res_name}/{scenario_name}/{anomaly_type}/{data_name}"
        else:
            path = f"{save_folder}/{scenario_name}/{anomaly_type}/{data_name}"

        try:
            os.makedirs(path)
        except:
            pass

        save_precision(self, path, repair_plot=plot_repairs)

