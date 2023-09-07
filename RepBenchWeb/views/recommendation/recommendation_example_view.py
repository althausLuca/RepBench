
from RepBenchWeb.models import TaskData
# from RepBenchWeb.celery import flaml_search_task, ray_tune_search_task

from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import time
from recommendation.ray_tune.ray_tune_config import config as ray_tune_config, RAYTUNE_ESTIMATORS
from recommendation.feature_extraction.feature_extraction import feature_endings
from recommendation.recommendation_input_loader import RecommendationInputLoader

from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']
feature_file_name = "features_train.csv"
recommendation_input_loader : RecommendationInputLoader = RecommendationInputLoader("features_train.csv")
X_train , y_train = recommendation_input_loader.get_train_data()
X_test , y_test = recommendation_input_loader.get_test_data()



#
# def start_raytunes(request):
#     automl_settings = {
#         "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
#         "task": 'classification',
#         "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
#     }
#
#
#     from RepBenchWeb.tasks import remove_ray_files
#     remove_ray_files.delay(0)
#
#
#     task_id = request.POST.get("task_id")
#     from RepBenchWeb.models import TaskData
#     try:  # clear older task running with same id
#         TaskData.objects.get(task_id=task_id).delete()
#     except TaskData.DoesNotExist:
#         pass
#
#     selected_features = dict(request.POST).get("ray_tunes_features")
#
#     selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
#     valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
#     features_in_X = [col_name for col_name in X_train.columns if any([col_name.endswith(end_) for end_ in valid_endings])]
#
#     estimator_list = dict(request.POST).get("ray_tunes_estimator_list")
#     estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
#     automl_settings["estimator_list"] = estimator_list
#
#     for estim_ in estimator_list:
#         assert estim_ in RAYTUNE_ESTIMATORS, f"Estimator {estim_} not supported by raytune found in {estimator_list}"
#
#     automl_settings["time_budget"] = 30
#     automl_settings["metric"] = request.POST.get("ray_tunes_metric", "accuracy")
#
#     task_data = TaskData(task_id=task_id, data_type="ray")
#     task_data.save()
#     optimizer = request.POST.get("ray_tunes_optimizer")
#     assert optimizer in ["default","ZOOpt","skopt","nevergrad","hyperopt"] , f"Optimizer {optimizer} not supported "
#     automl_settings["optimizer"] = optimizer
#
#
#
#     ray_tune_search_task.delay(automl_settings, X_train[features_in_X], y_train, X_test[features_in_X], y_test,
#                                my_task_id=task_id)
#
#     return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})
#
# def start_flaml(request):
#     automl_settings = {
#         "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
#         "task": 'classification',
#         "log_file_name": "recommendation/logs/flaml.log",
#         "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
#     }
#
#     token = request.POST.get("csrfmiddlewaretoken")
#     automl_settings["time_budget"] = int(request.POST.get("time_budget", 20))
#     automl_settings["metric"] = request.POST.get("metric", "accuracy")
#     automl_settings["task"] = "classification"
#
#     estimator_list = request.POST.get("estimator_list")
#     estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
#
#     automl_settings["estimator_list"] = estimator_list
#
#     task_id = request.POST.get("task_id")
#     from RepBenchWeb.models import TaskData
#     try:  # clear older task running with same id
#         TaskData.objects.get(task_id=task_id).delete()
#     except TaskData.DoesNotExist:
#         pass
#
#     selected_features = dict(request.POST).get("features")
#
#     selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
#     valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
#     features_in_X = [col_name for col_name in  X_train.columns if any([col_name.endswith(end_) for end_ in valid_endings])]
#     train_size = int(int(request.POST.get("train-size"))/(100) * len(X_train))
#     estimator_list = request.POST.get("estimator_list")
#     estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
#     automl_settings["estimator_list"] = estimator_list
#
#     task_data = TaskData(task_id=task_id, data_type="flaml")
#     task_data.save()
#     flaml_search_task.delay(automl_settings, X_train[features_in_X].iloc[:train_size,:], y_train[:train_size], X_test[features_in_X], y_test,
#                             my_task_id=task_id)
#
#     return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})
#

# def retrieve_flaml_results(request):
#     task_id = request.POST.get("task_id")
#
#     for i in range(25):
#         if TaskData.objects.filter(task_id=task_id).exists():
#             break
#         else:
#             time.sleep(0.3)
#
#
#     task_data = TaskData.objects.filter(task_id=task_id).last()
#     data = task_data.get_data()
#     status = task_data.status
#     if task_data.is_running():
#         return RepBenchJsonRespone({"data": data, "status": status})
#     if task_data.is_done():
#         # task_data.get_recommendation("test")
#         return RepBenchJsonRespone({"data": data, "status": status})


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
