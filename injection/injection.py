import numpy as np
import pandas as pd

from injection import inject_data_df
from injection.injected_data_container import InjectedDataContainer
from injection.label_generator import generate_df_labels
from recommendation.utils.file_parsers import read_file_to_pandas


def load_injected_container(injection_parameters, data_folder, row_cap=20000, col_cap=20, normalize=True):
    injected_df, truth_df = load_injected_data(injection_parameters, data_folder)
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
    print(col_range_map)
    assert injected_df.shape == truth_df.shape

    print("CHECK COL")
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

    # plt.plot(injected_df.iloc[:,:3])
    # plt.title("loaded injected")
    # plt.show()
    for injected_col in range(injected_df.shape[1]):
        print(np.isclose(injected_df.iloc[:, injected_col].values, truth_df.iloc[:, injected_col].values))
        # plt.plot(injected_df.iloc[:,0])
        # plt.plot(truth_df.iloc[:,0])
        # plt.show()

    class_df = pd.DataFrame(np.invert(np.isclose(truth_df.values, injected_df.values))
                            , index=injected_df.index, columns=injected_df.columns)

    assert class_df.isnull().sum().sum() == 0, (truth_df,)

    label_df: pd.DataFrame = generate_df_labels(class_df)

    assert class_df.index.equals(truth_df.index)
    assert label_df.index.equals(truth_df.index)

    assert injected_df.shape == truth_df.shape
    injected_container = InjectedDataContainer(injected_df, truth_df, class_df=class_df,
                                               name="repair_df",
                                               labels=label_df, check_rmse=container_does_rmse_checks)

    # plt.plot(injected_df.iloc[:,:3])
    # plt.title("loaded injected")
    # plt.show()

    return injected_container
