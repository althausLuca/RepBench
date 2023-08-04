import numpy as np

from RepBenchWeb.views.optimization.utils import extract_opt_input
from RepBenchWeb.views.task_view import TaskView
import json
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.tasks import succesive_halving_task
from RepBenchWeb.tasks import bayesian_optimization_task
from repair import algo_mapper
from repair.parameterization import BayesianOptimizer

class SuccesiveHalvingTask(TaskView):

    @classmethod
    def load_optimization_data(cls, setname, injected_series, row_limit=600):
        df_norm = DatasetView.load_data_container(setname).norm_data
        injected_data_container = injected_container_None_Series(df_norm, injected_series)

        truth = injected_data_container.truth
        injected = injected_data_container.injected
        labels = injected_data_container.labels
        columns_to_repair = injected_data_container.injected_columns

        repair_inputs = {
            "truth": truth.iloc[:row_limit, :],
            "injected": injected.iloc[:row_limit, :],
            "labels": labels.iloc[:row_limit, :],
            "injected_columns": columns_to_repair,
        }
        return repair_inputs

    @classmethod
    def specific_task(cls, request, task_id):
        print("starting specific task")

        alg_type, param_ranges = extract_opt_input(request.POST)

        post = request.POST.dict()
        # Bayesopt inputs
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post.get("error_loss", "rmse")

        injected_series = json.loads(post.pop("injected_series"))

        set_name = post.pop("setname")

        print("computing paramgrid")

        paramgrid = {}
        for k, v in param_ranges.items():
            if isinstance(v, tuple):
                if isinstance(v[0], int) and isinstance(v[0], int):
                    paramgrid[k] = np.arange(v[0], v[1] + 1)
                else:
                    paramgrid[k] = np.linspace(v[0], v[1], 10)
            else:
                paramgrid[k] = [v]

        opt_config = {}

        print("loading opt inputs")

        repair_inputs: dict = cls.load_optimization_data(set_name, injected_series)

        print("starting celery task")
        succesive_halving_task.delay(alg_type, paramgrid, opt_config,
                                     **repair_inputs,
                                     my_task_id=task_id)
        context = {
            "error_loss": error_loss,
            "alg_type": alg_type,
            "n_calls": n_calls,
            "n_initial_points": n_initial_points,
            "injected_series": injected_series,
            "param_ranges": param_ranges,
            "setname": set_name,
        }

        return RepBenchJsonRespone(context)




class BayesianOptimisationTask(SuccesiveHalvingTask):
    @classmethod
    def specific_task(cls, request, task_id):
        print("starting specific task")

        alg_type, param_ranges = extract_opt_input(request.POST)

        post = request.POST.dict()
        # Bayesopt inputs
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post.get("error_loss", "rmse")

        opt_config = {
            "n_initial_points": n_initial_points,
            "n_calls": n_calls,
            "error_score": error_loss,
        }

        injected_series = json.loads(post.pop("injected_series"))
        set_name = post.pop("setname")
        repair_inputs: dict = cls.load_optimization_data(set_name, injected_series)

        alg = algo_mapper[alg_type]()
        print("loading opt inputs")

        alg_params = alg.get_fitted_params()
        for key in param_ranges.keys():
            if key in alg_params.keys():
                d_type = type(alg_params[key])
                # cast data types to match alg_params
                min_ , max_  = param_ranges[key]
                param_ranges[key] = (d_type(min_), d_type(max_))

        optimizer = BayesianOptimizer(alg, **opt_config)  # just a test before running with celery

        print("starting celery task")
        bayesian_optimization_task.delay(alg_type, param_ranges, opt_config,
                                         **repair_inputs,
                                         my_task_id=task_id)
        context = {
            "error_loss": error_loss,
            "alg_type": alg_type,
            "n_calls": n_calls,
            "n_initial_points": n_initial_points,
            "injected_series": injected_series,
            "param_ranges": param_ranges,
            "setname": set_name,

        }

        return RepBenchJsonRespone(context)
