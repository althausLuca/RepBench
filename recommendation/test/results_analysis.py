import json
import math
import warnings
import pandas as pd
import sys
import os
import numpy as np
from flaml import AutoML
from matplotlib import pyplot as plt

from recommendation.utils import *


sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

feature_file_name = "recommendation/results/results_without_cd"


algorithms_scores: pd.DataFrame
feature_values: pd.DataFrame
best_algorithms: pd.DataFrame

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
data_sets = algorithms_scores["injection_parameters"]["dataset"]

algorithm_counts = best_algorithms.value_counts()

# fig, ax = plt.subplots(figsize=(10, 20))
# plt.scatter(best_algorithms,data_sets)
# plt.show()

no_alg_best = algorithms_scores["best_algorithm_error"] > algorithms_scores["original rmse"]["original rmse"]

best_algorithms[no_alg_best] = "No algorithm"

for injection_param in algorithms_scores["injection_parameters"]:
    try:

        data = algorithms_scores["injection_parameters"][injection_param]
        df = pd.DataFrame({'alg': best_algorithms, 'injection_param': data})

        # group the data by x and y and count the number of occurrences
        counts = df.groupby(['alg', 'injection_param']).size().reset_index(name='count')

        # create a scatter plot with counts as the size of the markers
        fig, ax = plt.subplots(figsize=(10, 20))

        plt.scatter(counts['alg'], counts['injection_param'], s= counts['count'])
        plt.title(injection_param)
        plt.show()
    except:
        print("no plot for " + injection_param)





# Out[5]:
# imr       13950
# screen     1329
# rpca        226
# cdrec       200
# Name: best_algorithm, dtype: int64
# best_algorithms = best_algorithms.values.flatten()
