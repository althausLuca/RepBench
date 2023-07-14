import sys

from skopt import gp_minimize
from repair.parameterization.optimizers.estimator_optimizer import EstimatorOptimizer


class BayesianOptimizer(EstimatorOptimizer):
    def __init__(self, repair_estimator, error_score : str , *, n_jobs=6, n_calls=40, n_initial_points=20, n_restarts_optimizer=0,
                 callback=None):
        self.n_calls = n_calls
        self.n_initial_points = n_initial_points
        self.n_restarts_optimizer = n_restarts_optimizer
        self.callback = callback
        super().__init__(repair_estimator, error_score, n_jobs=n_jobs)

    @staticmethod
    def convert_to_range(param_grid):
        param_ranges = {}

        # convert list to ranges
        for param_name, params_list in param_grid.items():
            if len(set(params_list)) == 1:
                param_ranges[param_name] = [params_list[0]]
            else:
                try:
                    [float(i) for i in params_list]  # check if all items are numerical arguments
                    min_, max_ = min(params_list), max(params_list)
                    if any([isinstance(elem, float) for elem in params_list]):
                        param_ranges[param_name] = (float(min_), float(max_))
                    else:
                        param_ranges[param_name] = (min_, max_)
                except ValueError:
                    param_ranges[param_name] = params_list

        return param_ranges

    def search(self, repair_inputs, param_grid, return_full_results=False):
        param_ranges = self.convert_to_range(param_grid)
        param_keys, param_values  = param_ranges.keys(), param_ranges.values() # split parameter values and keys

        self.iter_counter = 0

        def f(x):
            self.iter_counter += 1

            params = dict(zip(param_keys, x)) # recombine the parameter valuewith their names
            estim = self.estim_change_copy(params)
            score = estim.scores(**repair_inputs)[self.error_score]
            if self.iter_counter == self.n_initial_points:
                print("Finished initial points, computing most promising parameters")
            # print("params:" , params , "score:"  ,score)
            # sys.stdout.write(f"\rBayesian Optimization search {self.iter_counter / self.n_calls * 100:.1f} % {score}", )
            if self.callback is not None:
                self.callback({"params": params, "score": score, "iter": self.iter_counter})
            return score

        print("computing initial points (random sample)")
        gp_result = gp_minimize(f, param_values, n_initial_points=self.n_initial_points,
                                n_calls=self.n_calls + self.n_initial_points, n_jobs=-1)

        x_best = gp_result.x
        if return_full_results:
            return [dict(zip(param_keys, x_)) for x_ in gp_result.x_iters], gp_result.func_vals
        return dict(zip(param_keys, x_best))
