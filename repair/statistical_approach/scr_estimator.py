import pandas as pd

from repair.algorithms_config import SCR
from repair.estimator import Estimator
import numpy as np
import jpype


class SCREstimator(Estimator):

    def __init__(self, THETA: int = 5, delta: float = 1000, **kwargs):
        self.THETA = THETA
        self.delta = delta

    def get_fitted_params(self, **args):
        return {"THETA": self.THETA,
                "delta": self.delta,
                }

    def suggest_param_range(self, X):
        return {"THETA": [1, 3, 4, 5, 6, 10],
                "delta": [100, 1000, 5000]}

    def repair(self, injected, truth, columns_to_repair, labels=None):
        # truth = None
        repair = injected.copy()

        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath())

        jpype.addClassPath("./")
        print(jpype.getDefaultJVMPath())
        dp_runner = jpype.JClass('code.pythonEntryPoint')()

        columns_to_repair = [c for c in columns_to_repair if c < injected.shape[1]]
        for col in columns_to_repair:
            if injected.shape[0] < 1000:
                injected_np = np.array(injected.iloc[:, col])
                truth_np = np.array(truth.iloc[:, col])
                injected_java = jpype.JArray(jpype.JDouble)(injected_np)
                truth_java = jpype.JArray(jpype.JDouble)(truth_np)
                retval = dp_runner.start(self.THETA, self.delta, injected_java, truth_java)
                repair.iloc[:, col] = retval
            else:  # compute in batches
                for i, (batch_start, batch_end) in enumerate(
                        zip(range(0, len(injected), 1000), range(1000, len(injected), 1000))):

                    print("batchstart", batch_start, "batchend", batch_end)
                    injected_np = np.array(injected.iloc[batch_start:batch_end, col])
                    truth_np = np.array(truth.iloc[batch_start:batch_end, col])
                    injected_java = jpype.JArray(jpype.JDouble)(injected_np)
                    truth_java = jpype.JArray(jpype.JDouble)(truth_np)
                    retval = dp_runner.start(self.THETA, self.delta, injected_java, truth_java)

                    repair.iloc[batch_start:batch_end, col] = retval

        # jpype.shutdownJVM() "OSError: JVM cannot be restarted" if one tries to restart the JVM
        return repair


    @property
    def alg_type(self):
        return SCR

    def __str__(self):
        return f'SCR({round(self.THETA, 1)},{round(self.delta, 1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()
