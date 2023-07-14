import sys
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.flaml.flaml_search import flaml_search
from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/results_features"


algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

train_split_r = 0.8
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)

# get all other indices
test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
X_train = feature_values.iloc[train_split, :]
X_test = feature_values.iloc[test_split, :]
y_train, y_test = categories_encoded[train_split], categories_encoded[test_split]



time_budgets = [60]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--time_budgets', nargs='+', type=int, default=time_budgets,
                    help='Time budgets (in seconds) to use for FLAML search')

args = parser.parse_args()  # e.g --time_budgets 1200 3600
time_budgets = args.time_budgets

### Select features
n_features = [5] #, 10, 20, 25]

for k in n_features:
    for time_budget in time_budgets:
        automl_settings = {
            "time_budget": time_budget,  # in seconds
            "metric": "accuracy",  # accuracy , micro_f1, macro_f1
            "task": 'classification',
            "log_file_name": "recommendation/logs/flaml.log",
        }
        selector = SelectKBest(f_classif, k=k)
        selector.fit(X_train, y_train)
        cols_idxs = selector.get_support(indices=True)
        X_train_selected = X_train.iloc[:,cols_idxs].copy()
        selected_features = list(X_train_selected.columns)

        X_test_selected   = X_test[selected_features]

        flaml_search(automl_settings, X_train, y_train, verbose=2)
