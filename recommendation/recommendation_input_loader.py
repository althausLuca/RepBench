import numpy as np
import pandas as pd
from recommendation.feature_extraction.feature_extraction import feature_endings
from recommendation.utils import *
from recommendation.encoder import encode , decode

class RecommendationInputLoader:
    feature_folder = "recommendation/results/features"
    all_features = list(feature_endings.values())

    def __init__(self,
                 feature_file_name,
                 train_split_r=0.8,
                 features="all",
                 nan_safe=True,
                 include_anomaly_infos=False):

        if features == "all":
            features = self.all_features
        else:
            assert isinstance(features, list), "features must be a list of feature names"
            assert all([f in self.all_features for f in features]), f"features must be a subset of {self.all_features}"

        self.feature_file_name = feature_file_name
        self.feature_file_path = f"{self.feature_folder}/{feature_file_name}"
        self.train_split_r = train_split_r

        np.random.seed(0)

        algorithms_scores = parse_recommendation_results(self.feature_file_path)
        self.best_algorithms = algorithms_scores['best_algorithm']
        self.best_algorithms = encode(self.best_algorithms.values.flatten())


        assert  np.array_equal(decode(self.best_algorithms), algorithms_scores['best_algorithm'].values.flatten()), "decoding and encoding of algorithms failed"


        self.feature_values = algorithms_scores['features'].copy()

        all_close = lambda col: np.allclose(col.values, col.values[0])

        self.feature_names = [f_name for f_name in self.feature_values.columns
                              if any([f_name.endswith(f) for f in features])
                              and not all_close(self.feature_values[f_name])
                              ]

        self.feature_values = self.feature_values[self.feature_names]

        ## add anomaly infos as a feature:
        # if include_anomaly_infos:
        #     injection_params = algorithms_scores['injection_parameters']
        #     a_type = injection_params['a_type']
        #     factor = injection_params['factor']
        #     a_percent = injection_params['a_percent']
        #     # self.feature_values['a_type'] = a_type
        #     self.feature_values["factor"] = factor.to_list()
        #     self.feature_values['a_percent'] = a_percent.iloc[:].values


        self.categories_encoded = self.best_algorithms
        # self.labels = encoder.classes_
        # remove features with nan entries
        if nan_safe:
            #replace nan values with 0
            self.feature_values = self.feature_values.fillna(0)
            nan_free_rows = ~np.isnan(self.feature_values.values).any(axis=1)
            # print(np.isnan(self.feature_values.values).any(axis=1))
            self.feature_values = self.feature_values.iloc[nan_free_rows, :]
            self.categories_encoded = self.categories_encoded[nan_free_rows]

        ## Split data into train and test sets
        n_train_split = int(len(self.best_algorithms) * train_split_r)
        train_split = np.random.choice(len(self.feature_values), n_train_split, replace=False)
        # print(train_split)
        test_split = np.setdiff1d(np.arange(self.feature_values.shape[0]), train_split)
        # print(test_split)
        self.X_train: pd.DataFrame = self.feature_values.iloc[train_split, :]
        self.X_test: pd.DataFrame = self.feature_values.iloc[test_split, :]
        self.y_train, self.y_test = self.categories_encoded[train_split], self.categories_encoded[test_split]

        # check for NaN values
        assert not np.isnan(self.X_test.values).any(), self.X_test
        assert not np.isnan(self.X_train.values).any(), self.X_train


    def get_train_data(self,size_ratio=1):
        return self.X_train, self.y_train

    def get_test_data(self,size_ratio=1):
        return self.X_test, self.y_test