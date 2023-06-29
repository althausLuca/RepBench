import json

from django.http import JsonResponse
from django.shortcuts import render
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.forms.utils import parse_param_input
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.views.utils.cleanup_task import optimization_processes_queue_and_times, kill_process
from RepBenchWeb.models import TaskData

from RepBenchWeb.tasks import succesive_halving_task





class opt_JSONRespnse(JsonResponse):
    def __init__(self, data, callback=None, **kwargs):
        self.callback = callback
        super().__init__(data, encoder=self.NpEncoder, **kwargs)


class OptimizationView(DatasetView):
    template = OPTIMIZATION_TEMPLATE

    def create_opt_context(self, df):
        opt_context = {"bayesian_opt_form": BayesianOptForm(),
                       "b_opt_param_forms": optimization_param_forms_inputs(df),
                       "injection_form": InjectionForm(list(df.columns))}
        return opt_context

    def get(self, request, setname="BAFU"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.create_opt_context(df))
        return render(request, self.template, context=context)


def extract_opt_input(POST):
    algorithm = POST.get("algorithm")
    param_min_max_tuples = {}
    for k, v in dict(POST).items():
        print(k)
        print(type(k))
        splitted_input = k.split("-")
        if len(splitted_input) == 3:
            v = v if not isinstance(v,list) else v[0]
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


def start_optimization(request):
    token = request.POST.get("csrfmiddlewaretoken")
    alg_type, param_ranges = extract_opt_input(request.POST)
    print(dict(request.POST))

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
        TaskData.objects.get(task_id=token).delete()
    except TaskData.DoesNotExist:
        pass

    task_data = TaskData(task_id=token, data_type="ray")
    task_data.save()

    succesive_halving_task.delay(alg_type, injected, truth, labels, injected_columns=columns_to_repair,
                                 my_task_id=token, )
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


def fetch_opt_results(request):
    import time
    token = request.POST.get("csrfmiddlewaretoken")

    task_id = token

    for i in range(25):
        if TaskData.objects.filter(task_id=task_id).exists():
            break
        else:
            time.sleep(0.3)

    task_data = TaskData.objects.filter(task_id=task_id).last()
    data = task_data.data
    print(data)
    status = task_data.status
    if task_data.is_running():
        return RepBenchJsonRespone({"data": data, "status": status})
    if task_data.is_done():
        # task_data.get_recommendation("test")
        return RepBenchJsonRespone({"data": data, "status": status})

# def fetch_opt_results(request):
#     import psutil
#     status = "running"
#     token = request.GET.get("csrfmiddlewaretoken") or request.POST.get("csrfmiddlewaretoken")
#
#     if to_many_requests_response(token):
#         print("to many requests")
#         return RepBenchJsonRespone({"status": "DONE"})
#
#     try:
#         opt_process, out_put_queue, start_time = optimization_processes_queue_and_times[token]
#     except KeyError:
#         print("no process found")
#         return RepBenchJsonRespone({"results": [], "status": "DONE"})
#     results = []
#     try:
#         process = psutil.Process(opt_process.pid)
#         state = process.status()
#         data = out_put_queue.get(timeout=10, block=False)
#         res = data
#         res.update({"status": "running"})
#
#         return RepBenchJsonRespone(res)
#     except Empty:
#         status = "pending"
#
#     if not opt_process.is_alive():
#         optimization_processes_queue_and_times.pop(token, "")
#         opt_process.join()
#         status = "DONE"
#
#     return RepBenchJsonRespone({"results": results, "status": status})
