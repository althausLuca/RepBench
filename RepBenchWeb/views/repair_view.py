from django.shortcuts import render
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.config import DISPLAY_REPAIR_DATASETS_TEMPLATE
from RepBenchWeb.views.synthetic_dataset_view import SyntheticDatasetView
from repair import algo_mapper
from injection.injectedDataContainer import InjectedDataContainer
from testing_frame_work.data_methods.data_class import DataContainer
from testing_frame_work.repair import AnomalyRepairer
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.forms.alg_param_forms import SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField
from RepBenchWeb.forms.injection_form import InjectionForm, store_injection_form
import json
from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data
from RepBenchWeb.views.dataset_views import DatasetView


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


class RepairView(SyntheticDatasetView):
    template = "repair.html"
    error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_rmse": "RMSE on Anomaly",
                 "runtime": "runtime"}

    ParamForms = {"SCREEN": SCREENparamForm(), "RPCA": RPCAparamForm(), "CDrec": CDparamForm(), "IMR": IMRparamField()}


    def get(self, request, setname="BAFU"):
        data_object = InjectedContainer.objects.get(title=setname)
        injected_data_container: InjectedDataContainer = data_object.injected_container
        data_container = DataContainer(injected_data_container.truth)
        df = data_container.original_data
        context = {"setname": setname}
        context["data_info"] =  InjectedContainer.objects.get(title=setname).get_info()
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        context["alg_forms"] = self.ParamForms
        context["store_form"] = store_injection_form
        context["injection_form"] = InjectionForm(list(df.columns))
        context["injected_data_set_info"] = self.data_set_info_context(setname)
        return render(request, self.template, context=context)


    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        data_container = DatasetView.load_data_container(setname)

        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container = injected_container_None_Series(df_norm, injected_series)
        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]

        repair_scores = repair_retval["scores"]


        ###
        alg_constructor = algo_mapper[alg_type]
        alg_score = alg_constructor(**params).scores(**injected_data_container.repair_inputs)["rmse"]
        ###

        score_data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in repair_scores.items() if
                               k in RepairView.error_map.keys()]}

        metrics = list(repair_scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "score_data": score_data}

        links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}
        repaired_series = map_repair_data(repair, injected_data_container, alg_name, links, df_original)
        output = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        score_context = {
            "metrics": output["metrics"],
            "original_scores": injected_data_container.original_scores,
            "alg_name": alg_name
        }
        score_context.update(repair_scores)
        output["scores"] = score_context
        print("send repair data")
        return RepBenchJsonRespone(output)

    def repair_datasets(request=None, type="repair"):
        context = {}
        context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
                                        for dataSet in InjectedContainer.objects.all() if
                                        dataSet.title is not None and dataSet.title != "" }
        context["type"] = type
        return render(request, DISPLAY_REPAIR_DATASETS_TEMPLATE, context=context)
