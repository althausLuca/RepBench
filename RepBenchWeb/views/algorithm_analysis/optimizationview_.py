import json
import threading

from django.http import JsonResponse
from django.shortcuts import render
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.forms.optimization_forms import BayesianOptForm, optimization_param_forms_inputs
from RepBenchWeb.views.config import OPTIMIZATION_TEMPLATE
from RepBenchWeb.views.dataset_views import DatasetView

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
