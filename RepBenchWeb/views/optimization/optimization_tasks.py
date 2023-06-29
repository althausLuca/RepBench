from RepBenchWeb.views.task_view import TaskView

import json

from django.http import JsonResponse
from django.shortcuts import render
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.models import TaskData
from RepBenchWeb.tasks import succesive_halving_task

def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


class SuccesiveHalvingTask(TaskView):
    @classmethod
    def specific_task(cls, request,task_id):
        post = request.POST.dict()

        # Bayesopt inputs
        setname = post["setname"]
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post["error_loss"]
        alg_type = post.pop("alg_type")

        injected_series = json.loads(post.pop("injected_series"))
        param_ranges = {}

        # extract min and max ranges
        for key, v in post.items():
            if key.endswith("-min"):
                param_ranges[key.split("-")[0]] = parse_param_input(v)
        for key, v in post.items():
            if key.endswith("-max"):
                param_ranges[key.split("-")[0]] = (param_ranges[key.split("-")[0]], parse_param_input(v))

        df_norm = DatasetView.load_data_container(setname).norm_data
        injected_data_container = injected_container_None_Series(df_norm, injected_series)

        truth = injected_data_container.truth
        injected = injected_data_container.injected
        labels = injected_data_container.labels
        columns_to_repair = injected_data_container.injected_columns

        try:  # clear older task running with same id
            TaskData.objects.get(task_id=task_id).delete()
        except TaskData.DoesNotExist:
            pass

        task_data = TaskData(task_id=task_id, data_type="ray")
        task_data.save()

        succesive_halving_task.delay(alg_type, injected, truth, labels, injected_columns=columns_to_repair,
                                     my_task_id=task_id, )
        context = {
            "error_loss": error_loss,
            "alg_type": alg_type,
            "n_calls": n_calls,
            "n_initial_points": n_initial_points,
            "injected_series": injected_series,
            "param_ranges": param_ranges,
            "setname": setname,
        }
        return RepBenchJsonRespone(context)
