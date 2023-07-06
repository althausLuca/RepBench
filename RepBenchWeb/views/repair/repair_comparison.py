from django.shortcuts import render

from RepBenchWeb.forms.alg_param_forms import AlgorithmsForm
from RepBenchWeb.forms.dataset_forms import DataSetsForm
from RepBenchWeb.forms.injection_form import InjectionForm
from RepBenchWeb.models import DataSet
from RepBenchWeb.views.injection_view import InjectionView


class RepairAndCompare(InjectionView):
    template = "injectionAndRepair/inject_and_compare.html"

    def get(self, request):
        context = {}
        context["injection_form"] = InjectionForm([])
        context["algorithm_form"] = AlgorithmsForm()
        context["dataset_form"] = DataSetsForm()
        context["datasets_columns"] = {   dataset.title : list(dataset.df.columns) for dataset in DataSet.objects.all() }
        return render(request, self.template, context=context)