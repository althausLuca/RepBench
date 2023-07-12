import numpy as np
import pandas as pd

from injection.injection import create_injected_container

def injected_container_None_Series( truth_df , injected_series_dicts):
    injected_df = truth_df.copy()
    for series_dict in injected_series_dicts:
        col_name, data = series_dict["linkedTo"] ,  series_dict["data"]
        injected_data= np.array(data,dtype=float)
        values_to_repalce = ~np.isnan(injected_data)
        injected_df.loc[values_to_repalce,col_name] = injected_data[values_to_repalce]

    injected_data_container = create_injected_container(injected_df=injected_df,truth_df=truth_df)
    return injected_data_container



