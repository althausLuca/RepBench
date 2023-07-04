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

    # @staticmethod
    # def get_synthetic_data(request, setname):
    #     initial_visible_series = int(request.GET.get("initial_visible_series", 5))
    #     injected_data_container = SyntheticDatasetView.load_data_container(setname)
    #
    #     close = np.isclose(injected_data_container.truth, injected_data_container.injected)
    #     assert np.allclose(~close == injected_data_container.labels)
    #     print("assertion passed")
    #     assert False, "stop here"
    #
    #     df = injected_data_container.truth
    #     truth_container = DataContainer(df)
    #     result = {"series" : map_truth_data(truth_container, initial_visible_series=initial_visible_series) }
    #     cols = [i for i in df.columns]
    #     injected = injected_data_container.get_none_filled_injected()
    #     result["injected"] = [map_injected_series(injected[c],cols[i],truth_container) for i,c in enumerate(injected) if i in
    #                           injected_data_container.injected_columns]
    #     return RepBenchJsonRespone(result)
