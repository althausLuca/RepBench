import json
import pickle
from django.db import models
import pandas as pd
from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data
from injection.injectedDataContainer import InjectedDataContainer
from recommendation.recommend import get_recommendation, alg_names, get_recommendation_and_repair
from picklefield.fields import PickledObjectField
from RepBenchWeb.models.utils import *


class BaseDataSet(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    granularity = models.CharField(max_length=200, null=True, blank=True)
    additional_info = models.JSONField(default=dict ,null=True, blank=True)

    ## infered attributes
    ts_nbr = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    features = PickledObjectField(default=dict)

    def __init__(self, *args, **kwargs):
        super(BaseDataSet, self).__init__(*args, **kwargs)
        self.length, self.ts_nbr = self.df.shape

    class Meta:
        abstract = True

    def compute_features_(self):
        df = self.df
        from recommendation.feature_extraction.feature_extraction import extract_features
        features_ = {col: extract_features(df, column=i) for i, col in enumerate(df.columns)}
        self.features = features_

    def compute_features(self):
        self.compute_features_()
        self.save()

    def get_features(self):
        """
        Returns: dict of features for each column
        """
        # if self.features == {}:
        self.compute_features()
        return self.features

    @property
    def df(self):
        """
        Returns: pandas.DataFrame from stored json attribute
        """

        raise NotImplementedError("This method should be implemented in a subclass")

    def __str__(self):
        return self.title

    def get_info(self):
        raise NotImplementedError("This method should be implemented in a subclass")

    def get_info_(self):
        corr = self.df.corr().round(3)
        corr_data = []
        for i, row in enumerate(corr.values):
            for j, v in enumerate(row):
                corr_data.append([i, j, v])
        columns = self.df.columns.tolist()

        return {
            "length": self.length,
            "ts_nbr": self.ts_nbr,
            "values": self.length * self.ts_nbr,
            "title": self.title,
            "description": self.description,
            "granularity": self.granularity,
            "time_interval": granularity_to_time_interval(self.granularity),
            "columns": columns,
            "corr_data": corr_data,
        }

class DataSet(BaseDataSet):
    dataframe = models.JSONField(null=False, blank=False)
    ref_url = models.CharField(max_length=200, null=True, blank=True)
    url_text = models.CharField(max_length=200, null=True, blank=True)

    @property
    def df(self):
        """
        Returns: pandas.DataFrame from stored json attribute
        """

        json_data = self.dataframe
        # parse index values as numeric if possible

        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            data_frame = pd.read_json(self.dataframe)

        data_frame.columns = [c if isinstance(c, int) else c.replace(" ", "") for c in data_frame.columns]
        return data_frame

    def get_info(self):
        info: dict = self.get_info_()
        info["ref_url"] = self.ref_url
        info["url_text"] = self.url_text
        return info


class InjectedContainer(BaseDataSet):
    injectedContainer_json = models.JSONField(null=False, blank=False)
    original_data_set = models.CharField(max_length=100, null=True)
    granularity = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.JSONField(blank=True, null=True)  # recomendation for the model

    @property
    def injected_container(self):
        injected_container_: InjectedDataContainer = InjectedDataContainer.from_json(self.injectedContainer_json)
        return injected_container_

    @property
    def df(self):
        return self.injected_container.injected

    def get_info(self):
        injectedDataContainer: InjectedDataContainer = self.injected_container
        a_rates = injectedDataContainer.get_a_rate_per_col()
        a_nbr = injectedDataContainer.get_n_anomalies_per_col()
        scores = injectedDataContainer.original_scores
        scores = {score_map[k]: round(v, 4) for k, v in scores.items() if k in score_map.keys()}

        info = self.get_info_()
        info["injected_rates"] = {ts: r for ts, r in a_rates.items() if r > 0}
        info["a_nbr"] = {ts: n for ts, n in a_nbr.items() if n > 0}
        info["scores"] = scores
        info["original_data_set"] = self.original_data_set
        return info

    def recommendation_context(self, automl=None):
        features = self.get_features()

        # recommendation_dict = json.loads(self.recommendation)
        original_data = DataSet.objects.get(title=self.original_data_set)
        df_original = original_data.df
        injected_data_container = self.injected_container
        truth = injected_data_container.truth
        recommendation_results = get_recommendation_and_repair(injected_data_container, classifier=automl,
                                                               features=features)

        repairs = recommendation_results["alg_repairs"]
        repair_converted = {}
        for alg_name, repair in repairs.items():
            mean, std = truth.mean(), truth.std()  # injected.mean(), injected.std()
            repair_norm = (repair - mean) / std
            # normalize truth data w.r.t injected series
            repair_converted[alg_name] = map_repair_data(repair_norm, injected_data_container, alg_name=alg_name,
                                                         links=None, df_original=truth, distinct_ids=True)
        recommendation_results["alg_repairs"] = repair_converted

        # self.recommendation = json.dumps(recommendation_results, cls=)
        # self.save()

        return recommendation_results
