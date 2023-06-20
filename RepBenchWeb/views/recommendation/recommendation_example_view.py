# from django.core.cache import cache
from ray.tune.search.skopt import SkOptSearch
from sklearn.metrics import f1_score, accuracy_score

from RepBenchWeb.models import TaskData
from RepBenchWeb.celery import flaml_search_task, ray_tune_search_task

from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import sys
import os
import numpy as np
import time
from recommendation.ray_tune.ray_tune_config import config as ray_tune_config, RAYTUNE_ESTIMATORS
from recommendation.feature_extraction.feature_extraction import feature_endings
from recommendation.recommend import get_recommendation_and_repair
# sys.path.append(os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/validation_features"

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

train_split_r = 0.5
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)
test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)

X = feature_values
if X.isnull().values.any():
    nan_columns = X.columns[X.isnull().any()].tolist()
    if nan_columns:
        print("Columns containing NaN values:", nan_columns)

    nan_rows = X[X.isnull().any(axis=1)]
    if not nan_rows.empty:
        print("Row indices containing NaN values:\n", nan_rows.index)
    else:
        print("No rows contain NaN values.")
    print("X contains NaN values.")
    X = X.dropna(axis=1)

X_train = X.iloc[train_split, :]
X_test = X.iloc[test_split, :]

y_train: np.ndarray = best_algorithms[train_split]
y_test = best_algorithms[test_split]

from recommendation.encoder import encode

y_train = encode(y_train)
y_test = encode(y_test)
print(y_test, "y_test")
print(y_train, "y_train")


# print("YYY", y)
# from collections import Counter
# print(counter := Counter(y))

# get all other indices


def start_raytunes(request):
    automl_settings = {
        "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
        "task": 'classification',
        "log_file_name": "recommendation/logs/flaml.log",
        "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
    }


    from RepBenchWeb.tasks import remove_ray_files
    remove_ray_files.delay(0)


    task_id = request.POST.get("task_id")
    from RepBenchWeb.models import TaskData
    try:  # clear older task running with same id
        TaskData.objects.get(task_id=task_id).delete()
    except TaskData.DoesNotExist:
        pass

    selected_features = dict(request.POST).get("ray_tunes_features")

    selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
    valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
    features_in_X = [col_name for col_name in X.columns if any([col_name.endswith(end_) for end_ in valid_endings])]

    estimator_list = dict(request.POST).get("ray_tunes_estimator_list")
    print(estimator_list)
    estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
    automl_settings["estimator_list"] = estimator_list

    for estim_ in estimator_list:
        assert estim_ in RAYTUNE_ESTIMATORS, f"Estimator {estim_} not supported by raytune found in {estimator_list}"

    automl_settings["time_budget"] = 30
    automl_settings["metric"] = request.POST.get("ray_tunes_metric", "accuracy")

    task_data = TaskData(task_id=task_id, data_type="ray")
    task_data.save()
    optimizer = request.POST.get("ray_tunes_optimizer")
    assert optimizer in ["default","ZOOpt","skopt","nevergrad","hyperopt"] , f"Optimizer {optimizer} not supported "
    automl_settings["optimizer"] = optimizer

    # print("EEESTIMATOR", estimator_list)


    ray_tune_search_task.delay(automl_settings, X_train[features_in_X], y_train, X_test[features_in_X], y_test,
                               my_task_id=task_id)

    return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})

def start_flaml(request):
    automl_settings = {
        "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
        "task": 'classification',
        "log_file_name": "recommendation/logs/flaml.log",
        "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
    }

    token = request.POST.get("csrfmiddlewaretoken")
    automl_settings["time_budget"] = int(request.POST.get("time_budget", 20))
    automl_settings["metric"] = request.POST.get("metric", "accuracy")
    automl_settings["task"] = "classification"

    estimator_list = request.POST.get("estimator_list")
    estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")

    automl_settings["estimator_list"] = estimator_list

    task_id = request.POST.get("task_id")
    from RepBenchWeb.models import TaskData
    try:  # clear older task running with same id
        TaskData.objects.get(task_id=task_id).delete()
    except TaskData.DoesNotExist:
        pass

    selected_features = dict(request.POST).get("features")

    selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
    valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
    features_in_X = [col_name for col_name in X.columns if any([col_name.endswith(end_) for end_ in valid_endings])]

    estimator_list = request.POST.get("estimator_list")
    estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
    print(dict(request.POST))
    print("ESTIMATOR LIST", estimator_list)
    automl_settings["estimator_list"] = estimator_list

    task_data = TaskData(task_id=task_id, data_type="flaml")
    task_data.save()
    flaml_search_task.delay(automl_settings, X_train[features_in_X], y_train, X_test[features_in_X], y_test,
                            my_task_id=task_id)

    print("sarch task initialized")
    return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})


def retrieve_flaml_results(request):
    token = request.POST.get("csrfmiddlewaretoken")

    task_id = request.POST.get("task_id")
    # print("task_id retrive", task_id)

    for i in range(25):
        if TaskData.objects.filter(task_id=task_id).exists():
            break
        else:
            time.sleep(0.3)

    # print(TaskData.objects.filter(task_id=task_id))

    task_data = TaskData.objects.filter(task_id=task_id).last()
    data = task_data.get_data()
    status = task_data.status
    if task_data.is_running():
        return RepBenchJsonRespone({"data": data, "status": status})
    if task_data.is_done():
        # task_data.get_recommendation("test")
        return RepBenchJsonRespone({"data": data, "status": status})


def flaml_prediction(request, setname):
    task_id = request.POST.get("task_id")
    task_object = TaskData.objects.filter(task_id=task_id).last()
    # print("TAAASK OBKECT , ", task_object, task_id)

    classifier = task_object.get_classifier()
    from RepBenchWeb.models import InjectedContainer
    data_object = InjectedContainer.objects.get(title=setname)
    output = data_object.recommendation_context(classifier)

    # prediction = task_object.get_recommendation(setname)
    # response = get_recommendation_and_repair(prediction, setname)
    return RepBenchJsonRespone(output)
