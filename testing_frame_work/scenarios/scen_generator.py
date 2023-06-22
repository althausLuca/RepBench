import math
from pandas import DataFrame
import pandas as pd

from testing_frame_work.scenarios.scenario import Scenario
from injection.injectedDataContainer import InjectedDataContainer
import testing_frame_work.scenarios.scenario_config as sc
from injection.injection_methods import inject_data_df
from injection.utils.label_generator import generate_df_labels
from testing_frame_work.data_methods.data_class import DataContainer
import numpy as np

from itertools import accumulate


def gen_a_rate_data(df, a_type, cols):
    a_percentages = sc.scenario_specifications["a_percentages"]
    max_perc = max(a_percentages)
    a_percentages = sorted(a_percentages)
    injected_df, col_range_mapper = inject_data_df(df, a_type=a_type, cols=cols, a_percent=max_perc)
    n, _ = df.shape

    ### remove until anomaly ratio is lover than threshold
    col_range_mapper_rand = {col: np.random.permutation(index_list)
                             for col, index_list in col_range_mapper.items()}

    percentage_dict = {}
    for col in cols:
        column_ranges = col_range_mapper_rand[col]
        list_ratios = list(accumulate(column_ranges, lambda b, a: b + len(a) / n * 100, initial=0))
        list_ratios = np.array(list_ratios)
        last_index = 0
        for p in a_percentages:
            idx = np.abs(list_ratios - p).argmin()  # find closest ratio
            if last_index == idx or idx == 0:
                continue
            temp_df = percentage_dict.get(p, df.copy())
            percentage_dict[p] = temp_df
            last_index = idx
            ranges_to_replace = column_ranges[:idx]  # select all ranges under this ratio
            assert len(ranges_to_replace) > 0
            for range in ranges_to_replace:
                temp_df.iloc[range, col] = injected_df.iloc[range, col]

    ret_val = [(p, injected_df, df) for p, injected_df in percentage_dict.items()]
    return ret_val


def gen_a_size_data(df, a_type, cols):
    assert a_type != "outlier"
    a_lengths = sc.scenario_specifications["a_lengths"]
    max_length = max(a_lengths)

    n_anomalies = math.ceil(df.shape[0] / 1000)

    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df, a_type=a_type, cols=cols,
                                                   n_anomalies=n_anomalies, a_len=max_length)

    ret_val = []
    for a_length in a_lengths[:-1]:
        temp_df = injected_df.copy()
        for col in cols:
            for index_range in col_range_mapper[col]:
                temp_df.iloc[index_range[a_length:], col] = df.iloc[index_range[a_length:], col]

        ret_val.append((a_length, temp_df, df))
    ret_val.append((max_length, injected_df, df))
    return ret_val


def gen_ts_len_data(df, a_type, cols):
    ts_lengths_ratios = sc.scenario_specifications["length_ratios"]
    min_ratio = min(ts_lengths_ratios)
    n, m = df.shape
    offset = int((n - min_ratio * n) / 2)
    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df, cols=cols, a_type=a_type, offset=offset)
    ret_val = []

    for ratio in ts_lengths_ratios[:-1]:
        off_set = int((n - n * ratio) / 2)
        temp_df = injected_df.copy().iloc[off_set:-off_set, :]
        part_true_df = df.copy().iloc[off_set:-off_set, :]
        ret_val.append((ratio, temp_df, part_true_df))
    ret_val.append((1, injected_df, df))
    return ret_val


def gen_ts_nbr_data(df, a_type, cols):
    n_ts = sc.scenario_specifications["ts_nbrs"]
    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df, cols=[0], a_type=a_type)
    ret_val = []

    for n in n_ts:
        temp_df = injected_df.iloc[:, :n].copy()
        ret_val.append((n, temp_df, df.iloc[:, :n].copy()))
    return ret_val


def gen_a_factor_data(df, a_type, cols):
    a_factors = sc.scenario_specifications["a_factors"]
    a_factors = sorted(a_factors)
    ret_val = []
    minimal_factor = a_factors[0]

    seed = np.random.randint(1000)

    injected_df, col_range_mapper = inject_data_df(df.copy(), cols=cols, a_type=a_type, factor=minimal_factor,
                                                   seed=seed)
    ret_val.append((minimal_factor, injected_df, df))
    for f in a_factors[1:]:
        temp_df, _ = inject_data_df(df.copy(), cols=cols, a_type=a_type, factor=f, seed=seed)
        ret_val.append((f, temp_df, df))
    return ret_val


def gen_cts_nbr_data(df, a_type, cols):
    n_cts = sc.scenario_specifications["cts_nbrs"]
    n, m = df.shape
    full_injected_df = df.copy()
    full_injected_df, col_range_mapper = inject_data_df(full_injected_df, cols=list(range(m)), a_type=a_type)
    ret_val = []
    for m_c in sorted(n_cts):
        if m_c >= m:
            break
        temp_df = df.copy()
        temp_df.iloc[:, :m_c] = full_injected_df.iloc[:, :m_c]
        ret_val.append((m_c, temp_df, df))

    return ret_val


scen_generator_map = {
    sc.TS_NBR: gen_ts_nbr_data,
    sc.ANOMALY_SIZE: gen_a_size_data,
    sc.ANOMALY_RATE: gen_a_rate_data,
    sc.CTS_NBR: gen_cts_nbr_data,
    sc.TS_LENGTH: gen_ts_len_data,
    sc.ANOMALY_FACTOR: gen_a_factor_data
}


def build_scenario(scen_name, file_name, data_type, a_type, max_n_rows=None, max_n_cols=None, cols=None):
    assert scen_name in sc.SCENARIO_TYPES, f"scenario {scen_name} must be one of {sc.SCENARIO_TYPES}"
    if max_n_rows is None:  max_n_rows = sc.MAX_N_ROWS
    if max_n_cols is None: max_n_cols = sc.MAX_N_COLS

    data_container: DataContainer = DataContainer(file_name, data_type, max_n_rows, max_n_cols)
    np.random.seed(10)
    n, m = data_container.norm_data.shape
    if cols == "all":
        cols = list(range(m))
    assert max(cols) < m, f"column numbers {[i for i in cols if i >= m]} to high for {m} columns"

    data_frame = data_container.norm_data

    cols_to_inject = cols if cols is not None else [0]
    scen_data = scen_generator_map[scen_name](data_frame, a_type, cols_to_inject)
    scenario = Scenario(scen_name, file_name, a_type, data_container=data_container)

    for (name, injected_df, data_df) in scen_data:
        assert injected_df.index.equals(data_df.index), f"{injected_df.index},{data_df.index}"
        assert injected_df.shape == data_df.shape, f"{injected_df},{data_df}"

        class_df = pd.DataFrame(np.invert(np.isclose(data_df.values, injected_df.values))
                                , index=injected_df.index, columns=injected_df.columns)

        assert class_df.isnull().sum().sum() == 0, (data_df,)

        if scen_name not in ["cts_nbr"]:
            assert sum(class_df.sum(axis=0) != 0) == len(cols), f"{class_df.sum(axis=0)} \n  columns to inject {cols}"

        label_df: DataFrame = generate_df_labels(class_df)

        import matplotlib.pyplot as plt
        plt.plot(injected_df.iloc[:,cols_to_inject])
        plt.show()
        ##todo remove this once tested
        assert class_df.index.equals(data_df.index)
        assert label_df.index.equals(data_df.index)
        assert injected_df.shape == data_df.shape
        injdected_container = InjectedDataContainer(injected_df, data_df, class_df=class_df,
                                                    name=data_container.title,
                                                    labels=label_df)
        scenario.add_part_scenario(injdected_container, name)
    return scenario




