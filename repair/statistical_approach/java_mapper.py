import jpype
import time

import numpy as np
from matplotlib import pyplot as plt

jpype.startJVM(jpype.getDefaultJVMPath())
dp_runner = jpype.JClass('code.pythonEntryPoint')()

import pandas as pd
dirtyTimeSeries_np = pd.read_csv("data/stock1.2k.data", delimiter=",").values[:200,1]
truth_np =  pd.read_csv("data/stock1.2k.data", delimiter=",").values[:200,2]

## convert
dirtyTimeSeries = jpype.JArray(jpype.JDouble)(dirtyTimeSeries_np)
truth = jpype.JArray(jpype.JDouble)(truth_np)

print(start := time.time())
retval = dp_runner.start(5 , 300 ,dirtyTimeSeries,truth)
print(time.time() - start)
retval_np = np.array(retval)

jpype.shutdownJVM()

plt.plot(dirtyTimeSeries_np)
plt.plot(retval_np)
plt.plot(truth_np)
plt.legend(["dirty","repaired","truth"])
plt.show()


