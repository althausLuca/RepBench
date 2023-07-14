import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.utils import load_estimator
from recommendation.flaml.flaml_search import compute_automl_scores
from recommendation.recommendation_input_loader import RecommendationInputLoader



automl_file_folder = "recommendation/results/flaml_estimators"
store_folder = "recommendation/results/recommendation"


feature_file_name = "results_test_features_non_normalized"
recommendation_input = RecommendationInputLoader(feature_file_name,train_split_r=0.5)
X_test, y_test = recommendation_input.X_test, recommendation_input.y_test
X_train ,  y_train = recommendation_input.X_train, recommendation_input.y_train

label
for f in [os.listdir(automl_file_folder)[0]]:
    file_name = os.path.basename(f)
    automl = load_estimator(file_name)
    compute_automl_scores(automl,X_train,y_train, X_test, y_test,plot_confusion_matrix=True,labels=recommendation_input.labels)




label
recommendation_input = RecommendationInputLoader(feature_file_name,train_split_r=0.5,include_anomaly_infos=True)
X_test, y_test = recommendation_input.X_test, recommendation_input.y_test
X_train ,  y_train = recommendation_input.X_train, recommendation_input.y_train

for f in [os.listdir(automl_file_folder)[0]]:
    file_name = os.path.basename(f)
    automl = load_estimator(file_name)
    compute_automl_scores(automl,X_train,y_train, X_test, y_test,plot_confusion_matrix=True,labels=recommendation_input.labels)
