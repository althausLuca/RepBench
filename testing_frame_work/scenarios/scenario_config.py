##### Scenarios
BASE_SCENARIO = "base"
TS_LENGTH = "ts_len"
ANOMALY_SIZE = "a_size"
ANOMALY_RATE = "a_rate"
ANOMALY_FACTOR = "a_factor"
TS_NBR = "ts_nbr"
CTS_NBR = "cts_nbr"
SCENARIO_TYPES = [TS_LENGTH,ANOMALY_SIZE,ANOMALY_RATE,ANOMALY_FACTOR,TS_NBR,CTS_NBR]

MAX_N_ROWS = 20000
MAX_N_COLS = 10

scenario_specifications = {
    "length_ratios": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], #ts_len scenario
    "a_lengths" : [5, 10, 20, 40, 60, 80, 100, 200], # a_len scenario
    "a_percentages": [0.25, 0.5, 1, 2, 5, 10, 15, 20], #a_rate scenario
    "ts_nbrs": [3, 4, 5, 6, 7, 8, 9, 10], # TS number scenario
    "cts_nbrs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # cts_nbr scenario
    "a_factors": [0.5, 1, 2, 3, 4, 5, 10, 20], # a_factor scenario anomaly factor/amplitude compared to std of the data
}

### save folder
SAVE_FOLDER = "Results"