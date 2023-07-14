from celery import shared_task
from flaml import AutoML
import sys
import warnings

from sklearn.metrics import f1_score, accuracy_score

metrics = {
    "accuracy": accuracy_score,
    "micro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='micro'),
    "macro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro')
}

@shared_task(bind=True)
def flaml_search_task(self, settings, X_train, y_train, X_test, y_test, my_task_id):
    from RepBenchWeb.models import TaskData
    # automl = AutoML(**settings)
    normal_write = sys.stdout.write
    setting_metric = settings["metric"]
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)

    # for p_ in y_train:
    #     print(p_)
    def custom_metric(
            X_val, y_val, estimator, labels,
            X_train, y_train, weight_val=None, weight_train=None,
            *args,
    ):
        import time
        start = time.time()
        pred_time = (time.time() - start) / len(X_val)
        estimator.fit(X_train, y_train)
        y_pred = estimator.predict(X_val)
        score = metrics[setting_metric](y_pred, y_val)
        # print(y_pred,score)

        estimator_name = str(estimator.__class__.__name__).split("Estimator")[0]
        if estimator_name == "LRL1Classifier":
            estimator_name = "LogisticRegression"
        task_data.add_data({"score": score, "pred_time": pred_time,
                            "estimator": estimator_name, "config": {"model": estimator_name, **estimator.get_params()}})

        return score, {"pred_time": pred_time}

    # Initialize FLAML with custom metric
    automl = AutoML()

    settings["metric"] = custom_metric

    with warnings.catch_warnings():
        # warnings.simplefilter("ignore")
        automl.fit(X_train=X_train, y_train=y_train, X_val=X_test,y_val=y_test, **settings, n_jobs=3, verbose=-3)

    automl._state.metric = setting_metric  # reset metric to original (we cant picke local objects)

    task_data.set_classifier(automl)
    task_data.set_done()
    print("DONE")
