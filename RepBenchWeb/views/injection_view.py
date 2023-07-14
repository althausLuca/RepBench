import json
import random

from django.shortcuts import render

from RepBenchWeb.forms.file_upload import UploadFilesForm
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from injection.injectedDataContainer import InjectedDataContainer
from RepBenchWeb.forms.injection_form import store_injection_form, InjectionForm
from RepBenchWeb.models import InjectedContainer, DataSet
from RepBenchWeb.views.config import *
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.ts_manager.HighchartsMapper import map_injected_series
from RepBenchWeb.views.repair.repair_view import RepairView
from injection.injection_methods.basic_injections import add_anomalies
from testing_frame_work.data_methods.data_class import DataContainer
from RepBenchWeb.forms import ParamForms


class InjectionView(RepairView):
    template = INJECT_AND_REPAIR_TEMPLATE
    error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_rmse": "RMSE on Anomaly",
                 "runtime": "runtime"}

    def get(self, request, setname="BAFU"):
        data_object = DataSet.objects.get(title=setname)
        df = data_object.df
        context = {"setname": setname}
        context["data_info"] = data_object.get_info()
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        context["store_form"] = store_injection_form
        context["injection_form"] = InjectionForm(list(df.columns))
        context["alg_forms"] = ParamForms
        context["upload_form"] = UploadFilesForm()

        return render(request, self.template, context=context)



# @require_http_methods(["POST"])
def inject_data(request, setname):
    post = request.POST
    col_name = post.get("data_columns")

    data_object = DataSet.objects.get(title=setname)
    df = data_object.df
    title = data_object.title
    data_container = DataContainer(df, title=title)

    df = data_container.norm_data
    try:
        col_name = int(col_name)
    except:
        pass

    col_norm = df[col_name]
    original_col = data_container.original_data[col_name]

    # anomaly injection values
    factor = float(post.get("factor"))
    ratio = float(post.get("ratio"))
    a_type = post.get("anomaly")
    seed = post.get("seed")
    a_len = 30 # int(post.get("length"))
    if seed == '' or seed is None:
        seed = random.randint(0, 100)
    else:
        seed = int(seed)

    if a_type != "outlier":
        n_anomalies = int(ratio * df.shape[0] / 30) + 1
    else:
        n_anomalies = int(ratio * df.shape[0])

    col_injected_norm, _ = add_anomalies(col_norm,
                                         a_type=a_type,
                                         a_factor=factor,
                                         a_len=a_len,
                                         n_anomalies=n_anomalies,
                                         fill_na=True, seed=seed)
    col_injected = col_injected_norm * original_col.std() + original_col.mean()
    injected_series = map_injected_series(col_injected, col_injected_norm, col_name)
    return RepBenchJsonRespone({"injected_series": injected_series})


def store_data(request, setname):
    post = request.POST.dict()
    title = post.get("title")
    min, max = int(float(post.get("min"))), int(float(post.get("max")))
    if min < 0:
        min = 0

    visible = json.loads(post.get("visible_series"))
    description = post.get("description")
    post.pop("csrfmiddlewaretoken")

    data_object = DataSet.objects.get(title=setname)
    df = data_object.df
    granularity = data_object.granularity
    data_container =  DataContainer(df, title=title)

    df_norm = data_container.norm_data  # only work with normalized data
    df_original = data_container.original_data
    # df_original = data_container.original_data
    injected_series = json.loads(post.pop("injected_series"))
    selection_only = post.pop("selectionOnly", False)
    if selection_only:
        # cut min and max
        df_norm = df_norm.iloc[min:max]
        for series_dict in injected_series:
            series_dict["data"] = series_dict["data"][min:max]
            # only select visible series
            df_norm = df_norm[visible]
            df_original = df_original[visible]


    injected_data_container: InjectedDataContainer = injected_container_None_Series(df_norm, injected_series)
    injected_data_container.set_to_original_scale(df_original.mean(), df_original.std())

    if InjectedContainer.objects.filter(title=title).exists():
        InjectedContainer.objects.filter(title=title).delete()
    info = {}  # Set original title of setname

    injectedDataframe = injected_data_container.injected.to_json()
    injected_data_set = InjectedContainer(title=title, injectedContainer_json=injected_data_container.to_json(),
                                          description=description, original_data_set=setname,granularity= granularity)
    injected_data_set.save()
    return RepBenchJsonRespone({"success": True})


