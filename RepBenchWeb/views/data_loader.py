import numpy as np
from django.http import JsonResponse

from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from injection.injectedDataContainer import InjectedDataContainer
from RepBenchWeb.models import DataSet, InjectedContainer
from RepBenchWeb.ts_manager.HighchartsMapper import map_truth_data, map_injected_data_container
from testing_frame_work.data_methods.data_class import DataContainer


def load_data_container(setname,RepBenchWeb=4):
    if DataSet.objects.filter(title=setname).exists():
        data_object = DataSet.objects.get(title=setname)
        df = data_object.df
        title = data_object.title
        return DataContainer(df, title=title)
    try:
        injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container
    except InjectedContainer.DoesNotExist:
        raise ValueError(f"No dataset with name: {setname} found {InjectedContainer.objects.all()}")
    return DataContainer(injected_data_container.truth)


def get_data(request, setname,RepBenchWeb=4):
    RepBenchWeb = int(request.GET.get("RepBenchWeb", RepBenchWeb))
    if DataSet.objects.filter(title=setname).exists():
        df = DataSet.objects.get(title=setname).df
        return JsonResponse({ "series" : map_truth_data(df,RepBenchWeb=RepBenchWeb) })

    injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container

    close = np.isclose(injected_data_container.truth.values, injected_data_container.injected.values)
    assert np.allclose(~close, injected_data_container.class_df.values)
    results = map_injected_data_container(injected_data_container)
    return RepBenchJsonRespone(results)
