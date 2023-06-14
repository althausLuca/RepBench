import statsmodels.api as sm
import pandas as pd

data = sm.datasets.co2.load_pandas().data
data = data.reset_index(drop=True)

# Set the frequency and period for the time index
start_date = '2023-06-01'
freq = 'W'  # Hourly frequency

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
time_horizon = 500
split_idx = num_samples - time_horizon
train_df = data[:split_idx]  # train_df is a dataframe with two columns: timestamp and label
X_test = data[split_idx:]['index'].to_frame()  # X_test is a dataframe with dates for prediction
y_test = data[split_idx:]['co2']  # y_test is a series of the values corresponding to the dates for prediction

from flaml import AutoML

automl = AutoML()
settings = {
    "time_budget": 30,  # total running time in seconds
    "metric": 'mape',  # primary metric for validation: 'mape' is generally used for forecast tasks
    "task": 'ts_forecast',  # task type
    "log_file_name": 'CO2_forecast.log',  # flaml log file
    "eval_method": "holdout",  # validation method can be chosen from ['auto', 'holdout', 'cv']
    "seed": 7654321,  # random seed
}

automl.fit(dataframe=train_df,  # training data
           label='co2',  # label column
           period=time_horizon,  # key word argument 'period' must be included for forecast task)
           **settings)


flaml_y_pred = automl.predict(X_test)
import matplotlib.pyplot as plt

plt.plot(X_test, y_test, label='Actual level')
plt.plot(X_test, flaml_y_pred, label='FLAML forecast')
plt.xlabel('Date')
plt.ylabel('CO2 Levels')
plt.legend()
plt.show()