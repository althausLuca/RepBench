import sys
import os


sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.flaml.flaml_search import flaml_search
from recommendation.recommendation_input_loader import RecommendationInputLoader

feature_file_name = "try"

recommendation_input = RecommendationInputLoader(feature_file_name)

time_budgets = [180, 60 * 8]

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--time_budgets', nargs='+', type=int, default=time_budgets,
                    help='Time budgets (in seconds) to use for FLAML search')
args = parser.parse_args()  # e.g --time_budgets 1200 3600
time_budgets = args.time_budgets

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

metric = multiclass_metrics[0]
time_budget = 2

# for metric in multiclass_metrics:
# for time_budget in time_budgets:
automl_settings = {
    "time_budget": time_budget,  # in seconds
    "metric": metric,  # accuracy , micro_f1, macro_f1
    "task": 'classification',
    "log_file_name": "recommendation/logs/flaml.log",
    }
automl , filename = flaml_search(automl_settings, recommendation_input.X_train, recommendation_input.y_train, verbose=2,file_suffix="non_normalized")



