import json
import numpy as np
from django.shortcuts import render
from django.views import View
from RepBenchWeb.views.config import *
from RepBenchWeb.views import data_loader
import RepBenchWeb.models.datasetsConfig as datasetsConfig
from RepBenchWeb.models import DataSet, InjectedContainer

class DatasetView(View):
    default_nbr_of_ts_to_display = 5
    template = DISPLAY_DATASET_TEMPLATE
    # encoder = NpEncoder
    data_fetch_url_name = "get_data"
    load_data_container = data_loader.load_data_container

    def data_set_info_context(self, setname):
        dataSet = DataSet.objects.get(title=setname)

        # generatate correlation data for highcharts
        df = dataSet.df
        # corr = df.corr().round(3)
        # corr_data = []
        # for i, row in enumerate(corr.values):
        #     for j, v in enumerate(row):
        #         corr_data.append([i, j, v])
        # columns = df.columns.tolist()

        context = {}
        context["data_info"] = dataSet.get_info()
        # context["columns"] = columns
        # context["corr_data"] = corr_data
        # context.update(dataSet.get_catch_22_features())
        return context

    def data_set_default_context(self, request, setname=datasetsConfig.default_set):
        data_container = data_loader.load_data_container(setname)
        df = data_container.original_data
        context = {"setname": setname}
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        return context, df

    def get(self, request, setname=datasetsConfig.default_set):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_info_context(setname))
        return render(request, self.template, context=context)


# def sliders_view(request, setname="BAFU"):
#     from RepBenchWeb.catch22.features import features
#     dataSet = DataSet.objects.get(title=setname)
#     context = {} #dataSet.get_catch_22_features()
#     ## add abr and description to the features
#     for ts  , feature_dict  in context["catch22"].items():
#         for feature_name , feature_valued_dict in feature_dict.items():
#             feature_valued_dict['abr'] = features[feature_name]["abr"]
#             feature_valued_dict['description'] = features[feature_name]["description"]
#     return RepBenchJsonRespone(context)





def display_datasets(request=None,option="Display" , synthetic=False):
    context = {"datasets": {dataSet.title: dataSet.get_info()
                            for dataSet in DataSet.objects.all()},
               "syntheticDatasets": {dataSet.title: dataSet.get_info()
                                     for dataSet in InjectedContainer.objects.all() if
                                     dataSet.title is not None and dataSet.title != ""},

                "option" : option}


    if synthetic:
        return render(request, DISPLAY_DATASETS_SYNTHETIC_TEMPLATE, context=context)

    return render(request, DISPLAY_DATASETS_TEMPLATE, context=context)


def delete_dataset(request,setname):
    print("delete_dataset")
    print(setname)
    try:
        dataSet = DataSet.objects.get(title=setname)
        dataSet.delete()
        response = f"{setname} deleted"
        response = f"could not delete {setname}"
        raise Exception
    except:
        try:
            dataSet = InjectedContainer.objects.get(title=setname)
            print(dataSet,"EEEEEEEE")
            dataSet.delete()
            response = f"{setname} (synthetic) deleted"
        except Exception as e:
            print(f"could not delete {setname} in {DataSet.objects.all()} or {InjectedContainer.objects.all()}" )
            raise e
            response = f"could not delete {setname}"

    return display_datasets(request)
