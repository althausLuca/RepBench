import numpy as np
from RepBenchWeb.views.config import *
from RepBenchWeb.views.dataset_views import DatasetView
from RepBenchWeb.models import  InjectedContainer
from testing_frame_work.data_methods.data_class import DataContainer
from RepBenchWeb.ts_manager.HighchartsMapper import map_truth_data
from RepBenchWeb.utils.encoder import RepBenchJsonRespone


class SyntheticDatasetView(DatasetView):
    template = DISPLAY_DATASET_SYNTHETIC_TEMPLATE

    def data_set_info_context(self, setname):
        return {"data_info": InjectedContainer.objects.get(title=setname).get_info()}

