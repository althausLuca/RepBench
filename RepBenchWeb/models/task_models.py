import json
import pickle
import sqlite3
from django.db.utils import IntegrityError

from django.utils import timezone
from datetime import timedelta
from picklefield.fields import PickledObjectField
from django.db import models

from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.tasks.utils import revoke_task
from RepBenchWeb.utils.encoder import RepBenchJsonEncoder
from RepBenchWeb.views.recommendation.utils import get_relevant_parameters


class TaskData(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    data_type = models.CharField(max_length=255)
    data = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default="running")
    autoML = PickledObjectField(null=True, blank=True)

    def set_done(self):
        self.status = "done"
        self.save()

    def set_celery_task_id(self, celery_task_id):
        self.celery_task_id = celery_task_id
        self.save()

    def is_running(self):
        return self.status == "running"

    def is_done(self):
        return self.status == "done"

    def delete(self, *args, **kwargs):
        try:
            revoke_task(self.celery_task_id)
            print("old CELERY STOPPED")
        except:
            pass
        super().delete(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        task_id = kwargs.get('task_id')
        TaskData.objects.filter(task_id=task_id).delete()
        self.clean()
        super().__init__(*args, **kwargs)

    def add_data(self, data: dict):
        import time
        time = time.time()
        data["processed"] = False
        data["time"] = time
        self.data.append(json.loads(json.dumps(data, cls=RepBenchJsonEncoder)))
        self.save()

    def get_data(self):
        print("OOOOOOOOOOOOOOOOOOOOOII GETTING THE DATA")
        for i, data_iteration in enumerate(self.data):
            if not data_iteration["processed"]:
                try:
                    data_iteration["parameters"] = get_relevant_parameters(data_iteration.pop("config"))
                except KeyError:
                    pass  # no config
                data_iteration["processed"] = True
                if i > 0:
                    data_iteration["runtime"] = round(data_iteration["time"] - self.data[i - 1]["time"], 3)
                else:
                    data_iteration["runtime"] = round(data_iteration["time"] - self.created_at.timestamp(), 3)
        try:
            self.save()


        except (sqlite3.IntegrityError, IntegrityError):
            pass

        return self.data

    def clean(self):
        """ delete all objects older than 10 minutes"""
        time_threshold = timezone.now() - timedelta(minutes=30)
        TaskData.objects.filter(created_at__lt=time_threshold).delete()

    def set_classifier(self, classifier):
        print("SET AUTO ML classifier")
        self.autoML = pickle.dumps(classifier, pickle.HIGHEST_PROTOCOL)
        self.save()

    def get_classifier(self):
        return pickle.loads(self.autoML)

    # def get_recommendation(self, setname):
    #     automl = pickle.loads(self.autoML)
    #     return InjectedContainer.objects.get(title=setname).recommendation_context(automl)
    #
