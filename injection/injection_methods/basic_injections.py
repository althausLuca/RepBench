import numpy as np
from injection.injection_config import *
from injection.injection_methods.index_computations import get_random_indices
from injection.injection_methods.injection_error import InjectionError


def inject_point_outlier(data, indexes, factor, directions=(1, -1)):
    original_data = data.copy()
    data = np.array(data, dtype=np.float64)
    for index in indexes:
        data[index] += np.random.choice(directions) * np.random.normal(factor, scale=0.1)

    if np.allclose(data, original_data):
        raise InjectionError("No change in data after injection", anomaly_type=POINT_OUTLIER)
    return data


def inject_amplitude_shift(data, index_range, factor, directions=(1, -1)):
    original_data = data.copy()
    data[index_range] += np.random.choice(directions) * factor
    print(data)
    if np.allclose(data, original_data):
        raise InjectionError("No change in data after injection", anomaly_type=AMPLITUDE_SHIFT, data=data[index_range])
    return data


def inject_distortion(data, index_range, factor):
    original_data = data.copy()
    index_before = index_range[0] - 1
    first_element = data[min(index_before, 0)]
    data = np.array(data, dtype=np.float64)
    diff = np.diff(data[index_range], prepend=[first_element])
    diff[diff==0] = np.random.choice([-1,1],sum(diff==0))
    data[index_range] += (diff + np.sign(diff) / 2) * factor
    if np.allclose(data, original_data):
        raise InjectionError("No change in data after injection", data=data[index_range], anomaly_type=DISTORTION)
    return data

injection_mapper = {AMPLITUDE_SHIFT: inject_amplitude_shift,
                    DISTORTION: inject_distortion,
                    POINT_OUTLIER: inject_point_outlier}



def add_anomalies(original_column, a_type, *, n_anomalies, a_factor, a_len, offset=0, index_ranges=None, fill_na=False,
                  seed=None):
    if seed is not None:
        np.random.seed(seed)

    data_column = original_column.copy()
    if a_type == POINT_OUTLIER:
        a_len = 1

    if index_ranges is None:
        index_ranges = get_random_indices(len(data_column) - 2 * offset, a_len, n_anomalies)
        index_ranges = [arr + offset for arr in index_ranges]

    for index_range in index_ranges:
        data_column[index_range] = injection_mapper[a_type](data_column, index_range, factor=a_factor)[index_range]

    # for plotting only anomalies and connecting them with outside points
    if fill_na:
        anomalies = np.invert(np.isclose(data_column, original_column))
        to_fill = np.invert(np.convolve(anomalies, [True, True, True], "same"))
        data_column[to_fill] = None

    for index_range in index_ranges:
        assert not any(np.isclose(original_column[index_range],data_column[index_range]))

    return data_column, index_ranges
