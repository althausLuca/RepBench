import json
import threading

from django.http import JsonResponse
from django.shortcuts import render
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
# from RepBenchWeb.views.algorithm_analysis.optimiser_task import run_optimization
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.views.utils.cleanup_task import optimization_processes_queue_and_times, kill_process, \
    to_many_requests_response
from _queue import Empty


# def parse_param_input(p: str):
#     if p.isdigit():
#         return int(p)
#     try:
#         return float(p)
#     except:
#         return p


# class opt_JSONRespnse(JsonResponse):
#     def __init__(self, data, callback=None, **kwargs):
#         self.callback = callback
#         super().__init__(data, encoder=self.NpEncoder, **kwargs)


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


# def start_optimization(request, setname):
#     token = request.POST.get("csrfmiddlewaretoken")
#     print(token)
#     if token in optimization_processes_queue_and_times:
#         opt_process, opt_queue, opt_start_time = optimization_processes_queue_and_times[token]
#         print("Killing process")
#         kill_process(opt_process)
#         print("Killed process")
#         del optimization_processes_queue_and_times[token]
#
#     post = request.POST.dict()
#
#     # Bayesopt inputs
#     n_initial_points = int(post["n_initial_points"])
#     n_calls = int(post["n_calls"])
#     error_loss = post["error_loss"]
#     alg_type = post.pop("alg_type")
#
#     injected_series = json.loads(post.pop("injected_series"))
#     param_ranges = {}
#
#     # extract min and max ranges
#     for key, v in post.items():
#         if key.endswith("-min"):
#             param_ranges[key.split("-")[0]] = parse_param_input(v)
#     for key, v in post.items():
#         if key.endswith("-max"):
#             param_ranges[key.split("-")[0]] = (param_ranges[key.split("-")[0]], parse_param_input(v))
#
#     df_norm = DatasetView.load_data_container(setname).norm_data
#     injected_data_container = injected_container_None_Series(df_norm, injected_series)
#
#     opt_process, opt_queue, opt_start_time = run_optimization(alg_type=alg_type, n_calls=n_calls,
#                                                               n_initial_points=n_initial_points,
#                                                               injected_data_container=injected_data_container,
#                                                               param_ranges=param_ranges, error_loss=error_loss)
#
#     optimization_processes_queue_and_times[token] = (opt_process, opt_queue, opt_start_time)
#
#     context = {
#         "error_loss": error_loss,
#         "alg_type": alg_type,
#         "n_calls": n_calls,
#         "n_initial_points": n_initial_points,
#         "injected_series": injected_series,
#         "param_ranges": param_ranges,
#         "setname": setname,
#     }
#     return RepBenchJsonRespone(context)


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
