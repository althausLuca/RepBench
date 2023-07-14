import time

import pandas as pd
import numpy as np
import testing_frame_work.repair as alg_runner
from repair.IMR.IMR import imr
import matplotlib.pyplot  as plt
import matplotlib
matplotlib.use('TKAgg')

df = pd.read_csv("ild3k.data" , header=None)

index = df.iloc[:,0].values
injected = df.iloc[:,1].values
truth = df.iloc[:,3].values
y_0 = df.iloc[:,2].values
labels = df.iloc[:,4].values
repairer = alg_runner.AnomalyRepairer(1, 1)

#####
my_y_0 = injected.copy()
my_y_0[labels] = truth[labels]
assert all(my_y_0 == y_0)

###
labels = np.arange(len(labels))[labels]
start = time.time()
my_repair = imr(injected,my_y_0,labels=labels,tau = 0.01, p =1)["repair"]
start = time.time()

paper_alg_repair = pd.read_csv("p1delta0.01.csv" , header=None).iloc[:,0].values
diff = my_repair-paper_alg_repair
my_truth_diff = sum(abs( my_repair-truth))
paper_truth_diff = sum(abs( paper_alg_repair-truth))
print(my_truth_diff)
print(paper_truth_diff)


plt.plot(injected,color="red")
plt.plot(my_repair,color="blue")
plt.plot(paper_alg_repair,color="green")
plt.plot(my_repair-paper_alg_repair)
plt.show()

plt.plot(truth)
plt.plot(injected,color="red")
plt.show()
# norm_truth = (truth-mean)/std
# norm_injected = (injected-mean)/std
#
# anoms = np.invert(np.isclose(injected,truth))
# norm_truth[anoms]-norm_injected[anoms]


#
# my_repair = run_repair("imr",params={"tau":0.01, "p":1}, injected=injected,truth=truth,labels=labels,columns_to_repair=[0])["repair"]
# true_results = np.genfromtxt("p1delta0.01.csv",delimiter=',')
# assert  np.allclose(my_repair.values[:,0],true_results)
#
# my_repair= run_repair("imr",params={"tau":0.5, "p":2}, injected=injected,truth=truth,labels=labels,columns_to_repair=[0])["repair"]
# true_results = np.genfromtxt("p2delta0.5.csv",delimiter=',')
# assert  np.allclose(my_repair.values[:,0],true_results), sum(abs(my_repair.values[:,0]-true_results))
#
