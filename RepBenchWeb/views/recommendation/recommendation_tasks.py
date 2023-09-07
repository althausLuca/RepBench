from RepBenchWeb.views.task_view import TaskView

from RepBenchWeb.models import TaskData
from RepBenchWeb.tasks import flaml_search_task, ray_tune_search_task

from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import time
from recommendation.ray_tune.ray_tune_config import config as ray_tune_config, RAYTUNE_ESTIMATORS
from recommendation.feature_extraction.feature_extraction import feature_endings
from recommendation.recommendation_input_loader import RecommendationInputLoader


multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']
feature_file_name = "features_train.csv"
recommendation_input_loader : RecommendationInputLoader = RecommendationInputLoader("features_train.csv")
X_train , y_train = recommendation_input_loader.get_train_data()
X_test , y_test = recommendation_input_loader.get_test_data()


class FlamlTask(TaskView):

    @classmethod
    def specific_task(cls, request , task_id):
        automl_settings = {"metric": request.POST.get("metric", "accuracy"), "task": "classification",
                           "log_file_name": "recommendation/logs/flaml.log",
                           "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1'],
                           "time_budget": int(request.POST.get("time_budget", 20))}

        estimator_list = request.POST.get("estimator_list")
        estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")

        automl_settings["estimator_list"] = estimator_list

        selected_features = dict(request.POST).get("features")

        selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
        valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
        features_in_X = [col_name for col_name in  X_train.columns if any([col_name.endswith(end_) for end_ in valid_endings])]
        train_size = int(int(request.POST.get("train-size"))/(100) * len(X_train))
        estimator_list = request.POST.get("estimator_list")
        estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
        automl_settings["estimator_list"] = estimator_list

        task_data = TaskData(task_id=task_id, data_type="flaml")
        task_data.save()
        flaml_search_task.delay(automl_settings, X_train[features_in_X].iloc[:train_size,:], y_train[:train_size], X_test[features_in_X], y_test,
                                my_task_id=task_id)

        return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})

class RayTuneTask(TaskView):
    @classmethod
    def specific_task(cls, request, task_id):
        automl_settings = {
            "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
            "task": 'classification',
            "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
        }

        from RepBenchWeb.tasks import remove_ray_files
        remove_ray_files.delay(0)
        selected_features = dict(request.POST).get("ray_tunes_features")

        selected_features = selected_features if selected_features else []  ## if empty selection use an empty set and only multi dim
        valid_endings = [feature_endings[sel_] for sel_ in selected_features] + [feature_endings["multi_dim"]]
        features_in_X = [col_name for col_name in X_train.columns if
                         any([col_name.endswith(end_) for end_ in valid_endings])]

        estimator_list = dict(request.POST).get("ray_tunes_estimator_list")
        estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")
        automl_settings["estimator_list"] = estimator_list

        for estim_ in estimator_list:
            assert estim_ in RAYTUNE_ESTIMATORS, f"Estimator {estim_} not supported by raytune found in {estimator_list}"

        automl_settings["time_budget"] = 30
        automl_settings["metric"] = request.POST.get("ray_tunes_metric", "accuracy")

        task_data = TaskData(task_id=task_id, data_type="ray")
        task_data.save()
        optimizer = request.POST.get("ray_tunes_optimizer")
        assert optimizer in ["default", "ZOOpt", "skopt", "nevergrad",
                             "hyperopt"], f"Optimizer {optimizer} not supported "
        automl_settings["optimizer"] = optimizer


        ray_tune_search_task.delay(automl_settings, X_train[features_in_X], y_train, X_test[features_in_X], y_test,
                                   my_task_id=task_id)

        return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})
