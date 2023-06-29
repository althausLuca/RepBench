import itertools
import sys
import numpy as np
from repair.estimator import Estimator
from multiprocessing.pool import ThreadPool as Pool
import time


class EstimatorOptimizer():
    def __init__(self, repair_estimator, error_score ,*, n_jobs = 6):
        self.error_score = error_score
        self.estim: Estimator = repair_estimator
        self.n_jobs = n_jobs

    def estim_change_copy(self, param_dict):
        estim_copy = type(self.estim)(**param_dict)
        # estim_copy.__dict__.update(self.estim.__dict__)
        # estim_copy.__dict__.update(param_dict)
        return estim_copy


    def check_if_anomalous(self,repair_inputs):
        columns_to_repair = repair_inputs["columns_to_repair"]
        assert not np.allclose(repair_inputs["injected"].values[:, columns_to_repair],
                               repair_inputs["truth"].values[:, columns_to_repair])


    def find_optimal_params(self, repair_inputs : dict, param_grid : dict,) -> tuple:
        """ minimized the estimators repair score over the given parameter range"""
        self.check_if_anomalous(repair_inputs)
        start = time.time()
        found_params = self.search(repair_inputs,param_grid)
        search_time =  time.time() - start
        score = self.estim_change_copy(found_params).scores(**repair_inputs)[self.error_score]
        return found_params , search_time , score



    def search(self, repair_inputs,  param_grid):
        """

        Args:
            repair_inputs: dict with injected , truth  and labels (imr)
            param_grid: parameter dict { param_name : list , ...}

        Returns:

        """

        return self.grid(repair_inputs,param_grid)


    def dict_to_combonations(self,param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        return param_combinations

    def param_map(self,repair_inputs , param_combinations , run_time = False):
        """
        returns [(params , score )  , (params , score ,) .. ]
        """
        if isinstance(param_combinations,dict):
            param_combinations = self.dict_to_combonations(param_combinations)

        self.counter = 0
        n = len(param_combinations)

        def f(params):
            # self.counter += 1
            # sys.stdout.write(f"\rgrid search {self.counter /n * 100:.1f} %", )
            estim = self.estim_change_copy(params)
            score_ = estim.scores(**repair_inputs)[self.error_score]
            return score_

        if not run_time:
            with Pool(self.n_jobs) as p:
                scores =  np.array(p.map(f, param_combinations))
            return [(param_combinations[i] , scores[i]) for i in  np.argsort(scores)]

        result = []
        for params in param_combinations:
            start = time.time()
            score = f(params)
            end = time.time()
            result.append( (params,score,end-start) )
        return result



    def grid(self, repair_inputs, param_grid, combination_list = None):
        if combination_list is not None:
            param_combinations = combination_list
        else:
            param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))

        return  self.param_map(repair_inputs,param_combinations)[0][0]
