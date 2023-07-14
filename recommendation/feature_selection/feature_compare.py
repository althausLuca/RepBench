import sys
import os
import itertools


sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.recommendation_input_loader import RecommendationInputLoader
from recommendation.flaml.flaml_search import flaml_search, compute_automl_scores
from recommendation.feature_extraction.feature_extraction import feature_endings as ft_e

feature_file_name = "results_features"
multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

catch_22_feature_ending = ft_e['catch22']
ts_fresh_feature_ending = ft_e["tsfresh_minimal"]
multi_dim_feature_ending = ft_e["multi_dim"]
ts_fresh_selected_feature_ending = ft_e["tsfresh_selected"]

all_feature_lists = [[catch_22_feature_ending], [ts_fresh_feature_ending], [multi_dim_feature_ending],[ts_fresh_selected_feature_ending]]
feature_names_list = []

for i in range(1, 4):
    for f in itertools.combinations(all_feature_lists, i):
        feature_names_list.append(list(itertools.chain(*f)))

automl_settings = {
    "time_budget": 5*60,  # in seconds
    "metric": multiclass_metrics[0],  # accuracy , micro_f1, macro_f1 #https://stephenallwright.com/micro-vs-macro-f1-score/
    "task": 'classification',
    "log_file_name": "recommendation/logs/flaml.log",
}

for feature_endings in feature_names_list:
    for use_anom_info in [False,True]:
        # label
        recommendation_input = RecommendationInputLoader(feature_file_name , features=feature_endings , include_anomaly_infos=use_anom_info)
        automl, automl_name = flaml_search(automl_settings, recommendation_input.X_train, recommendation_input.y_train
                                           )

        compute_automl_scores(automl_name, recommendation_input.X_train, recommendation_input.y_train
                              , recommendation_input.X_test, recommendation_input.y_test,
                              plot_confusion_matrix=True,labels=recommendation_input.labels)
