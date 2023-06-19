##### Anomalies
AMPLITUDE_SHIFT = "shift"
DISTORTION = "distortion"
# GROWTH_CHANGE = "growth" # to handled by any algorithm yet
POINT_OUTLIER = "outlier"

ANOMALY_TYPES = (AMPLITUDE_SHIFT,
                 DISTORTION,
                 POINT_OUTLIER)

BASE_FACTORS = {AMPLITUDE_SHIFT: 2,
                DISTORTION: 2,
                POINT_OUTLIER: 3}

BASE_PERCENTAGES = {AMPLITUDE_SHIFT: 5,
                    DISTORTION: 5,
                    POINT_OUTLIER: 2
                    }


DEFAULT_LENGTH = 30  # ignored by point outliers

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





### imr labels
label_seed = 100
label_rate = 0.2
anomstartlabelrate = 0.2

#
# def parse_anomaly_name(type_name):
#     type_name = type_name.lower()
#     if type_name in ANOMALY_TYPES:
#         return type_name
#     a_min, v_min = -1, 100
#     for anom in ANOMALY_TYPES:
#         x = start_of_(type_name, anom)
#         if x < v_min:
#             a_min, v_min = anom, x
#     assert v_min < 100, f"could not parse anomaly anomaly type {type_name}"
#     return a_min
#
#
# def start_of_(str, type):
#     if len(str) == 0:
#         return 0
#     if len(type) == 0:
#         return 100
#
#     if str[0] == type[0]:
#         return start_of_(str[1:], type[1:])
#     else:
#         return start_of_(str, type[1:]) + 1
