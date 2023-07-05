import pandas as pd

from repair.Screen.globallp import LPconstrainedAE
from repair.Screen.screen import screen
from repair.algorithms_config import SCREEN
from repair.estimator import Estimator
import numpy as np


class SCREENEstimator(Estimator):

    def __init__(self, t:int=5, smax: float = 0.1, smin: float = None, ci=None ,**kwargs):
        """
        param ci need to be a tuple e.g (0.1,0.9)
        """

        self.smin = smin if smin is not None else -smax
        self.smax = smax
        self.t = t
        self.ci = ci

        assert self.smin <= 0
        assert self.smax >= 0

    def get_fitted_params(self, **args):
        return {"t": self.t,
             "smin": self.smin,
             "smax": self.smax,
                }

    def suggest_param_range(self, X):
        return {"smax": np.linspace(0, 1, num=20),
                "smin": -np.linspace(0, 1, num=20)}

    def repair(self, injected, truth, columns_to_repair, labels=None):
        truth = None
        repair = injected.copy()

        columns_to_repair = [c for c in columns_to_repair if c < injected.shape[1]]
        for col in columns_to_repair:
            x = np.array(injected.iloc[:, col])

            if self.ci is not None:
                self.ci =  (self.ci[0] if self.ci[0]>1 else self.ci[0]*100 ,
                            self.ci[1] if self.ci[1]>1 else self.ci[1]*100 )
                perc = np.percentile(sorted(np.diff(x)), tuple(self.ci))
                smax = perc[1]
                smin = perc[0]
                self.smax = smax
                self.smin = smin

            smin, smax = self.smin, self.smax
            repair_result = screen(x, self.t, smax, smin)

            repair.iloc[:, col] = repair_result
        return repair

    @property
    def alg_type(self):
        return  SCREEN

    def __str__(self):
        return f'SCREEN({self.t},{round(self.smax, 1)},{round(self.smin, 1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()
