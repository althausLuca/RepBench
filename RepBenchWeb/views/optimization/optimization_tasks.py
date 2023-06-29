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
import time
from RepBenchWeb.tasks import bayesian_optimization_task

def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


def extract_opt_input(POST):
    algorithm = POST.get("algorithm")
    param_min_max_tuples = {}
    for k, v in dict(POST).items():
        print(k)
        print(type(k))
        splitted_input = k.split("-")
        if len(splitted_input) == 3:
            v = v if not isinstance(v, list) else v[0]
            v = parse_param_input(v)
            alg_name, param_name, min_or_max = splitted_input
            if alg_name == algorithm:
                if min_or_max == "min":
                    if param_name in param_min_max_tuples:
                        param_min_max_tuples[param_name] = (v, param_min_max_tuples[param_name])
                    else:  ## max already asigned so make a tuple (min,max)
                        param_min_max_tuples[param_name] = v

                else:  ## must be max
                    if param_name in param_min_max_tuples:
                        param_min_max_tuples[param_name] = (param_min_max_tuples[param_name], v)
                    else:
                        param_min_max_tuples[param_name] = v

    return algorithm, param_min_max_tuples


class SuccesiveHalvingTask(TaskView):
    @classmethod
    def specific_task(cls, request, task_id):
        alg_type, param_ranges = extract_opt_input(request.POST)

        post = request.POST.dict()
        # Bayesopt inputs
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post["error_loss"]

        injected_series = json.loads(post.pop("injected_series"))

        setname = post.pop("setname")
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

    @staticmethod
    def fetch_data(request):
        task_id = request.POST.get("task_id", False) or request.POST.get("csrfmiddlewaretoken")

        for i in range(25):  # check that object is already created before directly running into an error
            if TaskData.objects.filter(task_id=task_id).exists():
                break
            else:
                time.sleep(0.3)

        task_data = TaskData.objects.filter(task_id=task_id).last()
        data = task_data.data
        status = task_data.status
        print("DAAAAAAAAATA", data, status)
        print("TAAAASK ID" , task_id)
        if task_data.is_running():
            return RepBenchJsonRespone({"data": data, "status": status})
        if task_data.is_done():
            # task_data.get_recommendation("test")
            return RepBenchJsonRespone({"data": data, "status": status})


class BayesianOptimisationTask(SuccesiveHalvingTask):
    @classmethod
    def specific_task(cls, request, task_id):
        alg_type, param_ranges = extract_opt_input(request.POST)

        post = request.POST.dict()
        # Bayesopt inputs
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post["error_loss"]

        injected_series = json.loads(post.pop("injected_series"))

        setname = post.pop("setname")
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

        paramgrid = param_ranges

        bayesian_optimization_task.delay(alg_type,paramgrid, injected, truth, labels, injected_columns=columns_to_repair,
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

