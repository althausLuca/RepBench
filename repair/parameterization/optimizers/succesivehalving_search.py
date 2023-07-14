import itertools
import numpy as np
import matplotlib.pyplot as plt
from repair.parameterization.optimizers.estimator_optimizer import EstimatorOptimizer


class SuccessiveHalvingOptimizer(EstimatorOptimizer):

    def __init__(self, repair_estimator, error_score: str, *, n_jobs=6, start_size=50, n_splits=1, callback=None):
        self.start_size = start_size
        self.n_splits = n_splits
        self.callback = callback
        super().__init__(repair_estimator, error_score, n_jobs=n_jobs)

    def search(self, repair_inputs, param_grid):

        start_size = self.start_size

        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        injected_full = repair_inputs["injected"]
        truth_full = repair_inputs["truth"]
        labels_full = repair_inputs["labels"]
        n, m = injected_full.shape

        anomaly_array = np.invert(np.isclose(injected_full, truth_full)).sum(axis=1)

        first_anomaly_index = np.argmax(anomaly_array)

        counter = 0
        while True:
            size = start_size
            print(f"iter_{counter} {len(param_combinations)} parameter combinations, data_size:{size}")


            start_index = first_anomaly_index - size / 2
            non_used_start = 0
            if start_index < 0:
                non_used_start = -start_index
                start_index = 0

            start_index = int(max(0, first_anomaly_index - size / 2))
            end_index = int(min(n, first_anomaly_index + size / 2 + non_used_start))
            # assert end_index - start_index == start_size , (start_index,end_index,start_size , first_anomaly_index)

            reduced_repair_indputs = {
                "injected": injected_full.iloc[start_index:end_index, :].copy(),
                "truth": truth_full.iloc[start_index:end_index, :].copy(),
                "labels": labels_full.iloc[start_index:end_index, :].copy(),
                "columns_to_repair": repair_inputs["columns_to_repair"]
            }

            # plt.plot(injected_full.iloc[start_index:end_index, repair_inputs["columns_to_repair"]])
            # plt.plot(truth_full.iloc[start_index:end_index, repair_inputs["columns_to_repair"]])
            # plt.title(f"iter_{counter} {len(param_combinations)} combinations")
            # plt.show()
            params_error = self.param_map(reduced_repair_indputs, param_combinations)
            avg_error = np.mean([error for _, error in params_error])
            # print("avg error:" , np.mean([error for _, error in params_error]), "Parameters:" ,params_error  )
            # reduce param combinations
            param_combinations = [params for i, (params, _) in enumerate(params_error) if i < len(params_error) / 2]
            # print("Kept parameters: " , param_combinations)

            #increase size
            start_size = start_size*2
            counter = counter + 1
            if self.callback is not None:
                self.callback(counter, param_combinations, size , params_error , avg_error , param_combinations)
            if len(param_combinations) < 5 or start_size > n:
                break

        # print(f"iter_{counter} {len(param_combinations)} parameter combinations data_size {size}")

        final_map = self.param_map(reduced_repair_indputs, param_combinations)
        final_parameters, score  =  self.param_map(reduced_repair_indputs,param_combinations)[0]
        # print("Final parameters: " , final_parameters)
        if self.callback is not None:
            self.callback(counter, [final_parameters], size, params_error, score, [final_parameters], final_parameters, score)

        return final_parameters
