import sys
import os

import numpy as np
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.flaml.flaml_search import flaml_search_multiprocess
from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/results_features"

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

train_split_r = 0.03
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)

# get all other indices
test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
X_train = feature_values.iloc[train_split, :]
X_test = feature_values.iloc[test_split, :]
y_train, y_test = categories_encoded[train_split], categories_encoded[test_split]

### Select features
k = 5
time_budget = 40
automl_settings = {
    "time_budget": time_budget,  # in seconds
    "metric": "accuracy",  # accuracy , micro_f1, macro_f1
    "task": 'classification',
    "log_file_name": "recommendation/logs/flaml.log",
}


flaml_process, out_put_queue = flaml_search_multiprocess(automl_settings, X_train, y_train)
# flaml_process_2 , out_put_queue_2 = flaml_search_multiprocess(automl_settings, X_train, y_train)

import re

#
regex = r"at\s+(\d+\.\d+)s,\s*estimator\s+(\w+)'s\s+best\s+error=(\d+\.\d+),\s*best\s+estimator\s+(\w+)'s\s+best\s+error=(\d+\.\d+)"

from _queue import Empty


while True:
    try:
        output = out_put_queue.get(timeout=10,block=False)
        if "at" in output:
            match = re.search(regex, output)
            if match:
                result = {"time": float(match.group(1)),
                          "estimator": match.group(2),
                          "error": float(match.group(3)),
                          "best_estimator": match.group(4),
                          "best_error": float(match.group(5))
                          }
                label
                print(output.split("cut")[-1] if "cut" in output else "")

    except Empty:
        if not flaml_process.is_alive():
            break

