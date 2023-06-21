import numpy as np
import pandas as pd

from injection.injectedDataContainer import InjectedDataContainer
from injection.injection_methods import inject_data_df
from injection.utils.label_generator import generate_df_labels
from recommendation.utils.file_parsers import read_file_to_pandas


def load_injected_container(injection_parameters, data_folder, row_cap=20000, col_cap=20, normalize=False):
    """
        Args:
        injection_parameters: dict = {
            "seed": seed,
            "factor": factor,
            "cols"(int): columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }

        data_folder (str): The path to the folder where the CSV dataset file is located inside "data" folder
        row_cap (int): The maximum number of rows to load from the dataset file (default is 20000).
        col_cap (int): The maximum number of columns to load from the dataset file (default is 20).
        normalize (bool): Whether to normalize the dataset (default is True).
    """
    injected_df, truth_df = load_injected_data(injection_parameters, data_folder, row_cap=row_cap, col_cap=col_cap,
                                               normalize=normalize)
    return create_injected_container(injected_df=injected_df, truth_df=truth_df, container_does_rmse_checks=True)


def load_injected_data(injection_parameters,
                       data_folder,
                       return_truth=True,
                       row_cap=20000, col_cap=20, normalize=True):
    """
    Args:
    injection_parameters: dict = {
            "seed": seed,
            "factor": factor,
            "cols" (int): columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }
        return_truth (bool): Whether to return the original dataset as well as the injected dataset
            (default is True).
        data_folder (str): The path to the folder where the CSV dataset file is located (default is
            default_data_folder).
        row_cap (int): The maximum number of rows to load from the dataset file (default is 20000).
        col_cap (int): The maximum number of columns to load from the dataset file (default is 20).

    Returns:
        If return_truth is True, returns a tuple containing two pandas DataFrames: the injected dataset
        and the original dataset (before injection). If return_truth is False, returns only the injected
        dataset as a pandas DataFrame.

    """
    injection_parameters = injection_parameters.copy()
    dataset = injection_parameters.pop("dataset")
    cols = injection_parameters["cols"]
    truth_df: pd.DataFrame = read_file_to_pandas(f"{data_folder}/{dataset}")

    # z-score  normalization and cutting
    n, m = truth_df.shape

    truth_df = truth_df.iloc[:min(n, row_cap), :min(m, col_cap)]
    truth_mean, truth_std = truth_df.mean(), truth_df.std()

    truth_df = (truth_df - truth_mean) / truth_std

    injected_df, col_range_map = inject_data_df(truth_df, **injection_parameters)
    assert injected_df.shape == truth_df.shape

    for injected_col in cols:
        assert not np.allclose(injected_df.iloc[:, injected_col].values, truth_df.iloc[:, injected_col].values)

    if not normalize:
        injected_df = injected_df * truth_std + truth_mean
        truth_df = truth_df * truth_std + truth_mean

    if return_truth:
        return injected_df, truth_df
    return injected_df


def create_injected_container(*, injected_df, truth_df, container_does_rmse_checks=True):
    """

    Args:
        injected_df: pd.DataFrame
        truth_df: pd-DataFrage
        container_does_rmse_checks (default = True): Make sure some values are anomalous

    Returns:
        InjectedDAtaContainer
    """
    assert injected_df.index.equals(truth_df.index), f"{injected_df.index},{truth_df.index}"
    assert injected_df.shape == truth_df.shape, f"{injected_df},{truth_df}"

    class_df = pd.DataFrame(np.invert(np.isclose(truth_df.values, injected_df.values))
                            , index=injected_df.index, columns=injected_df.columns)

    assert class_df.isnull().sum().sum() == 0, (truth_df,)

    label_df: pd.DataFrame = generate_df_labels(class_df)

    assert class_df.index.equals(truth_df.index)
    assert label_df.index.equals(truth_df.index)

    assert injected_df.shape == truth_df.shape
    injected_container = InjectedDataContainer(injected_df, truth_df, class_df=class_df,
                                               name="repair_df",
                                               labels=label_df)
    return injected_container
