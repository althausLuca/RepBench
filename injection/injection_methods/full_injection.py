import math

import numpy as np
import pandas as pd
from pandas import DataFrame

from injection.injectedDataContainer import InjectedDataContainer
from injection.injection_config import BASE_FACTORS, POINT_OUTLIER, BASE_PERCENTAGES, DEFAULT_LENGTH
from injection.injection_methods.basic_injections import add_anomalies
from injection.utils.label_generator import generate_df_labels
from testing_frame_work.data_methods.data_class import DataContainer


def inject_data_df(data_df, *, a_type, cols=None, offset=10,
                   factor=None, a_percent=None, n_anomalies=None,
                   a_len=None, index_range_col_mapper=None, seed=None):

    if factor is None:
        factor = BASE_FACTORS[a_type]
    if a_percent is None:
        a_percent = BASE_PERCENTAGES[a_type]
    if a_len is None:
        a_len = 1 if a_type == POINT_OUTLIER else DEFAULT_LENGTH
    if n_anomalies is None:
        assert a_percent > 0
        n_anomalies = math.floor(a_percent / 100 * data_df.shape[0] / a_len) + 1

    assert n_anomalies - int(n_anomalies) == 0

    columns_to_inject = [0] if cols is None else cols
    injected_df = data_df.copy()
    col_ranges_mapper = {}
    for col in columns_to_inject:
        column_to_inject = injected_df.iloc[:, col].copy().values
        injected_df.iloc[:, col], index_ranges = add_anomalies(column_to_inject, a_type, offset=offset,
                                                               a_factor=factor,
                                                               n_anomalies=n_anomalies, a_len=a_len,
                                                               index_ranges=None if
                                                               index_range_col_mapper is None else
                                                               index_range_col_mapper[col], seed=seed)
        assert not np.allclose(column_to_inject, injected_df.iloc[:, col]) , column_to_inject[index_ranges]
        col_ranges_mapper[col] = index_ranges
    assert injected_df.shape == data_df.shape
    assert injected_df.index.equals(data_df.index)
    return injected_df, col_ranges_mapper


def create_injected_DataContainer(file_name, data_type, *, a_type, cols=None):
    """
    Parameters:
    file_name : str
    data_type: str "test" or "train"
    Returns InjectedDataContainer containing the injected dataframe every thing is normalized
    -------
    """
    data_container: DataContainer = DataContainer(file_name, data_type)
    data_df = data_container.norm_data.copy()
    injected_df, _ = inject_data_df(data_df, a_type=a_type, cols=cols)
    class_df = pd.DataFrame(np.invert(np.isclose(data_df.values, injected_df.values)),
                            columns=data_df.columns).reindex_like(injected_df)
    label_df: DataFrame = generate_df_labels(class_df)

    assert injected_df.index.equals(data_df.index), f"{injected_df.index},{data_df.index}"
    assert class_df.index.equals(data_df.index)
    assert label_df.index.equals(data_df.index)

    return InjectedDataContainer(injected_df, data_container.norm_data, class_df=class_df, name=data_container.title,
                                 labels=label_df)



def get_injected_container_example():
    return create_injected_DataContainer("bafu5k", data_type="train",a_type="shift",cols=[0])
