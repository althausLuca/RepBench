import json


import os

from recommendation.feature_extraction.feature_extraction import extract_features
from injection import load_injected_data

default_data_folder = "recommendation/datasets/train"


def load_features(injection_parameters,data_folder):
    """
    param: injection_parameters: dict
       injection_parameters = {
            "seed": seed,
            "factor": factor,
            "cols": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }

    return: features: dict of features for the selected column
    """
    injected_df, _ = load_injected_data(injection_parameters, data_folder=data_folder)
    features = extract_features(injected_df, column=injection_parameters["cols"][0])
    return features

def get_injection_parameter_hashes_checker(file_name):
    if not os.path.exists(file_name):
        return lambda x: False

    with open(file_name, "r") as f:
        lines = f.readlines()

    injection_parameters_strings = set()
    for line in lines:
        injection_parameters = json.loads(line)["injection_parameters"]
        str_value = str(injection_parameters.values())
        injection_parameters_strings.add(str_value)

    def checker(injection_parameters):
        new_value = str(injection_parameters.values())
        return new_value in injection_parameters_strings

    return checker


def compute_features(load_filename,  store_filename, data_folder):
    """
    Args:
        load_filename (str): The path to the file containing the injection parameters.
        store_filename (str): The path to the file where the features will be stored.
        use_rawdata (bool): Whether undo normalization to compute the features (default is True).

    Returns:
        A list of dictionaries containing the injection parameters and the features for each injection.
    """

    if not os.path.exists(store_filename):
        os.makedirs(os.path.dirname(store_filename), exist_ok=True)

    with open(store_filename, "w") as f:
        f.write("")

    with open(load_filename, "r") as f:
        lines = f.readlines()
    results = []
    total_lines = len(lines)
    for i,line in enumerate(lines):
        results_line = json.loads(line)
        injection_parameters = results_line["injection_parameters"]
        features = load_features(injection_parameters,data_folder=data_folder)
        results_line["features"] = features
        results.append(results_line)
        # store result to file
        with open(store_filename, "a") as f:
            # for result in results:
            f.write(json.dumps(results_line) + "\n")
        show_progress_bar(i + 1, total_lines, prefix='Loading features:', suffix='Complete', length=50)
    return results

def show_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # label
    if iteration == total:
        print()
