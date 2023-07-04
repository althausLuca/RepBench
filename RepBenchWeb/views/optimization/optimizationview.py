import json

from django.shortcuts import render
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.forms.utils import parse_param_input
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.views.repair_view import RepairView
from RepBenchWeb.views.synthetic_dataset_view import SyntheticDatasetView


class OptimizationView(DatasetView):
    template = OPTIMIZATION_TEMPLATE

    def create_opt_context(self, df):
        opt_context = {"bayesian_opt_form": BayesianOptForm(),
                       "b_opt_param_forms": optimization_param_forms_inputs(df),
                       # "injection_form": InjectionForm(list(df.columns))
                       }
        return opt_context

    def data_set_info_context(self, setname):
        injected_container = InjectedContainer.objects.get(title=setname)
        df = injected_container.df
        context = {"data_info": injected_container.get_info()}
        context.update(self.create_opt_context(df))
        return context

