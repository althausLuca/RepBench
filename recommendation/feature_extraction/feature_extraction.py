import numpy as np
import pandas as pd
from pycatch22 import catch22_all
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters
from tsfresh import extract_features as tsfresh_extract_features
import re
from recommendation.feature_extraction.ts_fresh_features import selected_feature_names
import tsfel

feature_endings = {"catch22": "__ct",
                   "tsfresh_minimal": "__tsf_m",
                   "multi_dim": "__md",
                   "tsfresh_selected": "__tsf_s",
                   "tsfel": "__tsfel",
                   }


def extract_features(dataset: pd.DataFrame, column , replace_nan=True):
    """
    Extracts features from a dataset and returns them as a dictionary.
    Args:
        dataset: dataset to extract features from
        column: for which to extract features

    Returns:
        dictionary of features
    """
    dataset = (dataset - dataset.mean()) / dataset.std()  # normalize
    single_features = single_ts_feature_extraction(dataset.iloc[:, column].values)
    multi_features = multi_ts_feature_extraction(dataset, column)
    single_features.update(multi_features)

    if replace_nan:
        single_features = {k: v if not np.isnan(v) else 0 for k, v in single_features.items()}
    return single_features


def clean_feature_name(name):
    # replace any non-alphanumeric characters with an underscore
    return re.sub(r'\W+', '_', name)


def single_ts_feature_extraction(input_data):
    if isinstance(input_data, pd.Series):
        df_data = pd.DataFrame({'data': input_data.flatten()})
        np_data = df_data['data'].values
    else:
        assert isinstance(input_data, np.ndarray)
        np_data = input_data
        df_data = pd.DataFrame({'data': np_data.flatten()})

    features = {}
    selected_tsfresh_features = extract_selected_ts_fresh_features(np_data)
    tsfresh_features_minimal = extract_ts_fresh_features(np_data)
    catch22_features = extract_catch22_features(np_data)
    tsfel_features = extract_tsfel_features(np_data)

    features.update(catch22_features)
    features.update(tsfel_features)
    features.update(selected_tsfresh_features)
    features.update(tsfresh_features_minimal)
    return features


def multi_ts_feature_extraction(dataset: pd.DataFrame, column):
    n, m = dataset.shape

    corr: np.array = dataset.corr().values

    assert np.isnan(corr).sum() == 0, dataset

    col_corr = corr[:, column]
    col_corr__mean, col_corr_median = np.mean(col_corr), np.median(col_corr)
    col_corr_abs_mean, col_corr_abs_median = np.mean(np.abs(col_corr)), np.median(np.abs(col_corr))

    corr_abs_mean, corr_abs_median = np.mean(np.abs(corr)), np.median(np.abs(corr))
    n_ts = m

    # no nan values
    assert not np.isnan(col_corr__mean), corr
    assert not np.isnan(col_corr_median), corr
    assert not np.isnan(col_corr_abs_mean), corr
    assert not np.isnan(col_corr_abs_median), corr
    assert not np.isnan(corr_abs_mean), corr
    assert not np.isnan(corr_abs_median), corr

    multi_dim_features = {
        "col_corr__mean": col_corr__mean,
        "col_corr_median": col_corr_median,
        "col_corr_abs_mean": col_corr_abs_mean,
        "col_corr_abs_median": col_corr_abs_median,
        "corr_abs_mean": corr_abs_mean,
        "corr_abs_median": corr_abs_median,
        "n_ts": n_ts
    }
    multi_dim_features = {clean_feature_name(name) + feature_endings["multi_dim"]: val for name, val in
                          multi_dim_features.items()}
    return multi_dim_features


def extract_tsfel_features(data: np.ndarray):
    data = data.flatten()
    data = pd.DataFrame(data)
    cfg_file = tsfel.get_features_by_domain()
    tsfel_features = tsfel.time_series_features_extractor(cfg_file, data)
    tsfel_features = dict(zip(tsfel_features.columns, tsfel_features.values.flatten()))
    tsfel_features = {name.replace(" ", "_") + feature_endings["tsfel"]: round(val, 5) for name, val in tsfel_features.items()}
    # labeltsfel_features)

    return tsfel_features


def extract_catch22_features(data: np.ndarray):
    catch22_features = catch22_all(data)
    catch22_features = {clean_feature_name(name) + feature_endings["catch22"]: round(val, 4) for name, val in
                        zip(catch22_features["names"], catch22_features["values"])}

    return catch22_features


def extract_ts_fresh_features(data: np.ndarray, FCParameters=MinimalFCParameters()):
    data = data.flatten()
    timeseries = pd.DataFrame({"id": [0 for _ in range(len(data))],
                               "time": list(range(len(data))),
                               'data': data.flatten()}
                              )
    timeseries["id"] = timeseries["id"].astype(object)

    tsfresh_features = tsfresh_extract_features(timeseries, column_id="id", column_sort="time",
                                                default_fc_parameters=FCParameters,
                                                show_warnings=False,
                                                disable_progressbar=True)

    tsfresh_features_name = [
        clean_feature_name(s.replace('"', '').replace("data__", "")) + feature_endings["tsfresh_minimal"] for s in
        tsfresh_features.columns]
    tsfresh_features = dict(zip(tsfresh_features_name, tsfresh_features.values.flatten()))
    return tsfresh_features


def extract_selected_ts_fresh_features(data: np.ndarray):
    from recommendation.feature_extraction.ts_fresh_features import selected_ts_fresh_features
    data = data.flatten()
    timeseries = pd.DataFrame({"id": [0 for _ in range(len(data))],
                               "time": list(range(len(data))),
                               'data': data.flatten()}
                              )
    timeseries["id"] = timeseries["id"].astype(object)

    tsfresh_features = tsfresh_extract_features(timeseries, column_id="id", column_sort="time",
                                                default_fc_parameters=selected_ts_fresh_features)

    tsfresh_features_name = [
        clean_feature_name(s.replace('"', '').replace("data__", "")) + feature_endings["tsfresh_selected"] for s in
        tsfresh_features.columns]
    tsfresh_features = dict(zip(tsfresh_features_name, tsfresh_features.values.flatten()))

    return tsfresh_features
