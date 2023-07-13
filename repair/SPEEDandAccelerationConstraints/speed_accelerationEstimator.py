import pandas as pd

from repair import SCREENEstimator
from repair.algorithms_config import SCREEN, SPEEDandAcceleration
import numpy as np


class SpeedAndAccelerationEstimator(SCREENEstimator):

    def __init__(self, t: int = 3, smax: float = 0.1, smin=None, amax: float =1.0, amin=None, ci=None, **kwargs):

        """
        param ci need to be a tuple e.g (0.1,0.9)
        """
        self.amax = amax
        if amin is None:
            self.amin = -amax
        else:
            self.amin = amin
        super().__init__(t=t, smax=smax, smin=smin, ci=ci, **kwargs)

    def get_fitted_params(self, **args):
        return {"t": self.t,
                "smin": self.smin,
                "smax": self.smax,
                "amin": self.amin,
                "amax": self.amax,
                }

    def suggest_param_range(self, X):
        return {"smax": np.linspace(2/20, 2, num=20),
                "amax": np.linspace(1/20, 4, num=20), }

    def repair(self, injected, truth, columns_to_repair, labels=None):
        truth = None
        repair = injected.copy()

        columns_to_repair = [c for c in columns_to_repair if c < injected.shape[1]]
        for col in columns_to_repair:
            x = np.array(injected.iloc[:, col])

            if self.ci is not None:
                self.ci = (self.ci[0] if self.ci[0] > 1 else self.ci[0] * 100,
                           self.ci[1] if self.ci[1] > 1 else self.ci[1] * 100)
                perc = np.percentile(sorted(np.diff(x)), tuple(self.ci))
                smax = perc[1]
                smin = perc[0]
                self.smax = smax
                self.smin = smin

            smin, smax = self.smin, self.smax
            from repair.SPEEDandAccelerationConstraints.algorithm1 import algorithm1
            repair_result = algorithm1(x, smin=smin, smax=smax, amin=self.amin, amax=self.amax, w=self.t)

            repair.iloc[:, col] = repair_result
        return repair

    @property
    def alg_type(self):
        return SPEEDandAcceleration

    def __str__(self):
        return f'{self.alg_type}({self.t},{round(self.smax, 1)},{round(self.smin, 1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()
