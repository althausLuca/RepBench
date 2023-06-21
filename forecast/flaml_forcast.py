import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def forecast(data, col_name, plot_name):
    # Set the frequency and period for the time index

    if not pd.api.types.is_datetime64_any_dtype(data.index):
        data = data.reset_index(drop=True)

        # Set the frequency and period for the time index
        start_date = '2020-06-01'
        freq = '60s'  # Hourly frequency

        # Generate the time index using pd.date_range()
        num_rows = len(data)
        time_index = pd.date_range(start=start_date, periods=num_rows, freq=freq)

        data.index = time_index
        # data['index'] = time_index
        data.reset_index(inplace=True)

        # data is given in weeks, but the task is to predict monthly, so use monthly averages instead
        # data = data['co2'].resample('MS').mean()
    data = data.bfill().ffill()  # makes sure there are no missing values
    # data = data.to_frame().reset_index()
    num_samples = data.shape[0]
    time_horizon = int(num_samples * 0.25)
    split_idx = num_samples - time_horizon
    train_df = data.iloc[:split_idx]  # train_df is a dataframe with two columns: timestamp and label
    X_test = data.iloc[split_idx:]['index'].to_frame()  # X_test is a dataframe with dates for prediction
    y_test = data.iloc[split_idx:][
        col_name]  # y_test is a series of the values corresponding to the dates for prediction

    from flaml import AutoML

    automl = AutoML()
    settings = {
        "time_budget": 100,  # total running time in seconds
        "metric": 'rmse',  # primary metric for validation: 'mape' is generally used for forecast tasks
        "task": 'ts_forecast',  # task type
        # "log_file_name": 'CO2_forecast.log',  # flaml log file
        "eval_method": "holdout",  # validation method can be chosen from ['auto', 'holdout', 'cv']
        "seed": 7654321,  # random seed
        # "estimator_list": ,
    }

    automl.fit(dataframe=train_df,  # training data
               label=col_name,  # label column
               period=time_horizon,  # key word argument 'period' must be included for forecast task)
               **settings)

    flaml_y_pred = automl.predict(X_test)

    plt.plot(X_test, y_test, label='Actual level')
    plt.plot(X_test, flaml_y_pred, label='FLAML forecast')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.legend()
    plt.title(plot_name)
    plt.show()

    return automl, X_test, y_test


from testing_frame_work.data_methods.data_class import DataContainer
from injection.injection_config import AMPLITUDE_SHIFT
from injection.injection_methods import inject_data_df

file_name = "elec.csv"
data_container: DataContainer = DataContainer(file_name, "train")

data_frame = data_container.norm_data
anomaly_type = AMPLITUDE_SHIFT

injected_df = data_frame.copy()

injected_col = 0

num_samples = data_frame.shape[0]
time_horizon = int(num_samples * 0.25)

injected_df.iloc[:time_horizon], col_range_mapper = inject_data_df(injected_df.iloc[:time_horizon], a_type=anomaly_type,
                                                                   cols=[injected_col],
                                                                   a_percent=10, a_len=40)

injected_col_name = injected_df.columns[injected_col]

plt.plot(injected_df[injected_col_name], label='Injected level')
plt.plot(data_frame[injected_col_name], label='Actual level')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.show()

automl, X_test, y_test = forecast(injected_df.iloc[:, [injected_col]], col_name=injected_col_name, plot_name="injected")



for col, ranges in col_range_mapper.items():
    for range in ranges:
        injected_df.iloc[range,col] = np.NaN
    injected_df.iloc[:, col] = injected_df.iloc[:, col].interpolate()

automl, X_test, y_test = forecast(injected_df.iloc[:, [injected_col]], col_name=injected_col_name, plot_name="interpolated")


automl, X_test, y_test = forecast(data_frame.iloc[:, [injected_col]], col_name=injected_col_name, plot_name="true")
