import pandas as pd
import sys
import os
from sktime.datasets import load_from_tsfile
import warnings

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..',
                 '..')))  # run from top dir with  python3 recommendation/score_retrival.py

# Set the filename and read the file

mode = "test"
folder = "recommendation/datasets/Multivariate_ts/"
store_folder = f"recommendation/datasets/{mode}/"

for data_folder in os.listdir(folder):
    data_set = data_folder  # "BasicMotions"


    filename = folder + data_set + "/" + data_set + "_" + mode.upper() + ".ts"

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            train_x, train_y = load_from_tsfile(
                filename, return_data_type='numpy2D'
            )

            groups = list(set(train_y))
            dummy_groups = [train_y == group for group in groups]
            dfs = [pd.DataFrame(train_x[group, :].T) for group in dummy_groups]
            for df, group in zip(dfs, groups):
                df = df.iloc[:min(df.shape[0], 20000), :min(30, df.shape[1])]
                if df.shape[0] >= 100:
                    df.to_csv(store_folder + data_set + f"_{group}.csv", index=False)
            if df.shape[0] >= 100:
                with open("recommendation/datasets/sktime_data_sets.txt", "a") as f:
                    f.write(data_folder + "\n")

    except ValueError as  e :

        pass
