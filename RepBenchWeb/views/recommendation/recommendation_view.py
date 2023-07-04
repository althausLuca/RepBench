from django.shortcuts import render

from RepBenchWeb.forms.dataset_forms import InjectedDataSetForm
from RepBenchWeb.views.config import *
from RepBenchWeb.forms.recommendation_forms import FLAMLSettingsForm, RayTuneSettingsForm
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.views.synthetic_dataset_view import SyntheticDatasetView


class RecommendationView(SyntheticDatasetView):
    templates = [FLAML_RECOMMENDATION_TEMPLATE, RAY_TUNE_RECOMMENDATION_TEMPLATE]
    recommender_file_name = ""

    def get(self, request, type="FLAML"):
        context = {}
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        context["flaml_settings_form"] = FLAMLSettingsForm()
        context["ray_tune_settings_form"] = RayTuneSettingsForm()
        context["injected_datasets_form"] = InjectedDataSetForm()

        if type == "FLAML":
            template = self.templates[0]
        else:
            template = self.templates[1]

        return render(request, template, context=context)

    @staticmethod
    def recommendation_datasets(request=None):
        context = {}
        context["datasets"] = {dataSet.title: dataSet.get_info()
                                        for dataSet in InjectedContainer.objects.all() if
                                        dataSet.title is not None and dataSet.title != "" }
        context["type"] = "recommendation"
        return render(request, 'dataSetOptions/displayRecommendationDatasets.html', context=context)
