import argparse

import numpy as np
import pandas as pd
import os

from injection.injection_methods import inject_data_df
from testing_frame_work.data_methods.data_class import DataContainer
from injection.injection_config import ANOMALY_TYPES


STORE_FOLDER = "injection/Results"


try: #make folder if does not exist
    os.mkdir(STORE_FOLDER)
except:
    pass

DATA_FOLDER = "full"

def add_injection_arguments_to_parser(parser):
    parser.add_argument('-a','-anomaly_type',  required=True , choices=ANOMALY_TYPES , help='anomaly type')
    parser.add_argument("-f", "-a_factor",  required=True)
    parser.add_argument("-r", "-ratio",  required=True)
    parser.add_argument("-ts" ,"-time_series")
    parser.add_argument("-d" , "-dataset", required=True)
    parser.add_argument("-l" , "-length" , default="30" ,type = int)

def init_injection_parser(input = None):
    parser = argparse.ArgumentParser()
    add_injection_arguments_to_parser(parser)
    if input is not None:
        args = parser.parse_args(input.split())
    else:
        args = parser.parse_args()

    return args


def main(input = None):
    print("starting injection")
    parser = init_injection_parser(input)
    file_name =  parser.d
    factor = float(parser.f)
    ratio = float(parser.r)
    ts = parser.ts
    cols = [int(col.strip()) - 1 for col in ts.split(",")]
    print(cols)
    a_type = parser.a



    data_container: DataContainer = DataContainer(file_name, DATA_FOLDER)
    original_data = data_container.original_data
    norm_data = data_container.norm_data
    injected_df_norm : pd.DataFrame
    injected_df_norm , _ = inject_data_df(data_df=norm_data,a_type=a_type,cols=cols ,a_percent=ratio,factor=factor)
    print("injected container created")
    injected_df : pd.DataFrame  = injected_df_norm*original_data.std() + original_data.mean()
    file_name = file_name if file_name.endswith(".csv") else file_name + ".csv"
    print("load csv")
    injected_df.to_csv(f"{STORE_FOLDER}/{file_name}", index=False)
    print("csv generated")


    # checks that injected series values differ from original series values
    # and remain the same on the non injected series

    injected_values = injected_df.values
    original_values = original_data.values
    assert not np.allclose(injected_values, original_values)
    assert not np.allclose(injected_df_norm.values, norm_data.values)

    injected_values[:,cols] = 0
    original_values[:,cols] = 0

    assert np.allclose(injected_values, original_values) , injected_values-original_values
    print("checks passes")



if __name__ == "__main__":
    main()
