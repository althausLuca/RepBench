import numpy as np
import pandas as pd
from pandas import DataFrame

from injection.injectedDataContainer import InjectedDataContainer
from testing_frame_work.data_methods.data_class import DataContainer


## mapping to highcharts series
def map_truth_data(original_data: pd.DataFrame, norm_data: pd.DataFrame = None, RepBenchWeb=5):
    df, df_norm = original_data, norm_data \
        if norm_data is not None else (original_data - original_data.mean()) / original_data.std()


    data =  [{"visible": i < RepBenchWeb, "id": col_name, "name": col_name, "data": list(df[col_name])
                       , "norm_data": list(df_norm[col_name])}
             for (i, col_name) in enumerate(df.columns)]

    return data

def map_injected_series(injected_series: pd.Series, injected_series_norm: pd.Series, original_column: str):
    """
    map injected pandas series containing values only in anomalies
    and points next to anomalies to highcharts series
    """
    print("map_injected_series")
    return {"linkedTo": original_column,
            "id": f"{original_column}_injected",
            "name": f"{original_column}_injected",
            "data": injected_series.replace({np.nan: None}).values.tolist(),
            "norm_data": injected_series_norm.replace({np.nan: None}).values.tolist(),
            "color": "red",
            "dashStyle": "ShortDot",

            }


def map_injected_data_container(injected_data_container: InjectedDataContainer):
    print("map_injected_data_container")

    truth: pd.DataFrame = injected_data_container.truth
    injected: pd.DataFrame = injected_data_container.injected

    # normalize injected data
    mean, std = truth.mean() , truth.std() #injected.mean(), injected.std()
    injected_norm = (injected - mean) / std
    # normalize truth data w.r.t injected series
    truth_norm = (truth - mean) / std

    truth_series = map_truth_data(truth, truth_norm)
    injected_series = []
    injected_data_container.get_none_filled_injected()
    for i, col_name in enumerate(injected.columns):
        if i not in injected_data_container.injected_columns:
            continue
        injected_col, injected_col_norm = injected[col_name], injected_norm[col_name]
        class_col = injected_data_container.class_df[col_name].values
        class_col_extended = ~(np.convolve(class_col, [1, 1, 1], mode="same") > 0)
        injected_col.loc[class_col_extended] = np.nan
        injected_col_norm.loc[class_col_extended] = np.nan

        injected_series.append(
            map_injected_series(injected_col, injected_col_norm, col_name)
        )

    return {"series": truth_series, "injected": injected_series}


def map_repair_data(repair: DataFrame, injected_data_container: InjectedDataContainer, alg_name: str,
                    links: dict, df_original: DataFrame):

    truth = injected_data_container.truth
    repair.columns = truth.columns
    injected_data_container: InjectedDataContainer
    data = {
        str(col_name) + "repair": {**({"linkedTo": links[col_name]} if links else {}),
                                   "id": str(col_name) + "repair" + alg_name,
                                   "name": alg_name.split("(")[0],
                                   "data": list(reverse_norm(repair[col_name], df_original[col_name])),
                                   "norm_data": list(repair[col_name]),
                                   "original_series_col": col_name,
                                   "legendIndex": -1,
                                   "showInLegend": True
                                   }
        for (i, col_name) in enumerate(injected_data_container.truth.columns) if
        i in injected_data_container.injected_columns}

    return data


def reverse_norm(norm_data, original_data):
    return norm_data * original_data.std() + original_data.mean()
