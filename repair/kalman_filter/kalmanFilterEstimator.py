import numpy as np

from repair import Estimator
from repair.algorithms_config import KalmanFilter


class KalmanFilterEstimator(Estimator):

    def __init__(self, transition_cov: float = 0.5, threshold : float =-1.0,  **kwargs):
        #default is not threshold (threshold=-1.0) means that we don't use threshold and just return the smoothed result
        self.transition_cov = transition_cov
        self.threshold = threshold
        # super().__init__(**kwargs)

    def get_fitted_params(self, **args):
        return {"transition_cov": self.transition_cov,
                "threshold": self.threshold,
                }

    def suggest_param_range(self, X):
        return {"transition_cov": np.linspace(1 / 20, 1, num=20),
                "threshold" : np.linspace(2 / 20, 2, num=20)
             }

    def repair(self, injected, truth, columns_to_repair, labels=None):
        truth = None
        repair = injected.copy()

        columns_to_repair = [c for c in columns_to_repair if c < injected.shape[1]]
        for col in columns_to_repair:
            x = np.array(injected.iloc[:, col])
            from repair.kalman_filter.kalman_filter import kalman_filter
            repair_result = kalman_filter(x, transition_covariance=self.transition_cov)

            if self.threshold > 0:
                repair.iloc[:, col] = repair_result
            else:
                diff = np.abs(repair_result-x)
                norm_diff = (diff - np.mean(diff))/np.std(diff)
                values_to_replace = norm_diff > self.threshold
                repair.iloc[values_to_replace, col] = repair_result[values_to_replace]

        return repair

    @property
    def alg_type(self):
        return KalmanFilter

    def __str__(self):
        if self.threshold is None:
            return f'{self.alg_type}({self.transition_cov})'
        return f'{self.alg_type}({self.transition_cov},{self.threshold})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()
