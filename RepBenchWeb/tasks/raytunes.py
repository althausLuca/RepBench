from sklearn.metrics import f1_score, accuracy_score
import numpy as np
from ray.tune.search.hyperopt import HyperOptSearch
from ray.tune.search.nevergrad import NevergradSearch
from ray.tune.search.skopt import SkOptSearch
from celery import shared_task, signals
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
import celery


metrics = {
    "accuracy": accuracy_score,
    "micro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='micro'),
    "macro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro')
}

import ray
from ray.tune import Callback
from ray import tune, air
from ray.tune.search.zoopt import ZOOptSearch



# ### Raytune does not work when celery is used for some reason (because of the logging setup)
# @signals.setup_logging.connect
# def setup_celery_logging(**kwargs):  #disble default celery logging setup for ray tunes to function
#     pass
# @celery.signals.after_setup_logger.connect
# def on_after_setup_logger(**kwargs): ## add some  logging
#     logger = logging.getLogger('celery')
#     logger.propagate = True
#     logger = logging.getLogger('celery.app.trace')
#     logger.propagate = True


#
# import logging
# class TaskFilter(logging.Filter):
#     def filter(self, record):
#         task_name = getattr(record, 'task_name', '')
#         return task_name != 'RepBenchWeb.tasks.raytunes.ray_tune_search_task'


@shared_task(bind=True)
def ray_tune_search_task(self, settings, X_train, y_train, X_test, y_text, my_task_id):

    from RepBenchWeb.models import TaskData

    # logger = logging.getLogger(__name__)
    # logger.addFilter(TaskFilter())



    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)

    X = X_train
    y = y_train


    setting_metric = settings["metric"]

    class MyCallback(Callback):
        def on_trial_result(self, iteration, trials, trial, result, **info):
            data_ = {"score": result["score"],
                     "estimator": result["config"]["model"],
                     "pred_time": result["time_this_iter_s"],
                     "config": result["config"].copy()
                     }

            task_data.add_data(data_)

    def train_model(config):
        estimator = config.get("model")
        if estimator == "RandomForest":
            model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                           max_depth=config["max_depth"],
                                           min_samples_split=config["min_samples_split"])
        elif estimator == "ExtraTrees":
            model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
                                         max_depth=config["max_depth"],
                                         min_samples_split=config["min_samples_split"],
                                         max_features=config["max_features"])

        elif estimator == "LogisticRegression":
            model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')

        else:  # "LGBM"
            model = LGBMClassifier(n_estimators=config["n_estimators"],
                                   num_leaves=config["num_leaves"],
                                   learning_rate=config["learning_rate"],
                                   min_child_samples=config["min_child_samples"])
        model.fit(X, y)
        y_predict = model.predict(X_test)
        score = metrics[setting_metric](y_text, y_predict)
        return {"score": score}

    ray_tune_config = {
        "model": tune.choice(settings["estimator_list"]),
        "n_estimators": tune.randint(5, 30),
        "max_depth": tune.randint(3, 10),
        "min_samples_split": tune.randint(2, 6),
        "num_leaves": tune.randint(2, 30),
        "learning_rate": tune.choice(np.logspace(-4, 0, 500)),
        "min_child_samples": tune.randint(3, 15),
        "C": tune.choice(np.logspace(-5, 0, 500)),  # tune.loguniform(1e-3, 1)
        "max_features": tune.randint(3, 30),
        "max_leaf_nodes": tune.randint(3, 20),
    }

    search_alg = settings["optimizer"]

    if search_alg == "ZOOpt":
        zoopt_search_config = {
            "parallel_num": 3  # how many workers to parallel
        }

        zoopt_search = ZOOptSearch(
            algo="Asracos",  # only support Asracos currently
            budget=500000,  # must match `num_samples` in `tune.TuneConfig()`.
            # dim_dict=dim_dict,
            metric="score",
            mode="max",
            **zoopt_search_config
        )
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=50000, metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=500000, search_alg=zoopt_search))
    elif search_alg == "skopt":
        skopt_search = SkOptSearch(
            metric="score",
            mode="max",
        )

        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=skopt_search))

    elif search_alg == "nevergrad":
        import nevergrad as ng
        ng_search = NevergradSearch(
            optimizer=ng.optimizers.OnePlusOne,
            metric="score",
            mode="max",
        )

        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=ng_search))
    elif search_alg == "hyperopt":
        hyperopt_search = HyperOptSearch(
            metric="score", mode="max",
        )
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=hyperopt_search))

    elif search_alg == "default":
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000 ))

    result_grid = tuner.fit()
    best_result = result_grid.get_best_result()
    best_config = best_result.config

    estimator = best_config.get("model", "LGBM")
    if estimator == "RandomForest":
        model = RandomForestClassifier(n_estimators=best_config["n_estimators"],
                                       max_depth=best_config["max_depth"],
                                       min_samples_split=best_config["min_samples_split"])
    elif estimator == "ExtraTrees":
        model = ExtraTreesClassifier(n_estimators=best_config["n_estimators"],
                                     max_depth=best_config["max_depth"],
                                     min_samples_split=best_config["min_samples_split"])
    elif estimator == "LogisticRegression":
        model = LogisticRegression(penalty="l1", C=best_config["C"], solver='liblinear')

    else:  # "LGBM"
        model = LGBMClassifier(n_estimators=best_config["n_estimators"],
                               num_leaves=best_config["num_leaves"],
                               learning_rate=best_config["learning_rate"],
                               min_child_samples=best_config["min_child_samples"])


    model.fit(X, y)
    task_data.set_done()
    print("DONE")
    task_data.set_classifier(model)