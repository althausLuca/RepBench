from collections import defaultdict
"""
Names of the algorithms
If you change any name make sure to modify parameters.toml accordingly
This name will be shown in the webtool and plots
"""
IMR = "IMR"
SCREEN = "SCREEN"
RPCA = "RPCA"
Robust_PCA = RPCA
CDREP = "CDREP"
SCR = "SCR"
KalmanFilter = "KFilter"
SPEEDandAcceleration = "SCREEN2"

ALGORITHM_TYPES = (IMR, SCREEN, RPCA, CDREP, SPEEDandAcceleration, SCR, KalmanFilter)
MAIN_ALGORITHMS = (IMR, SCREEN, RPCA, CDREP, KalmanFilter)

# aliases for the algorithms names
AlgorithmAliases = {IMR: ["imr"],
                    SCREEN: ["screen","speed"],
                    RPCA: ["rpca"],
                    CDREP: ["cdrep"],
                    KalmanFilter: ["kfilter"],
                    SPEEDandAcceleration: ["screen*"],
                    SCR: ["scr"]}

AlgorithmAliases = defaultdict(lambda: [], AlgorithmAliases)


# black is used for the truth, and red for anomalies
ALGORITHM_COLORS = {IMR: "blue", SCREEN: "purple", RPCA: "green", CDREP: "orange", KalmanFilter: "brown",
                    SPEEDandAcceleration: "pink"}
ALGORITHM_COLORS = defaultdict(lambda: 'cyan', ALGORITHM_COLORS)


## metrics
RMSE = "rmse"
PARTIAL_RMSE = "rmse_partial"  # only on the anomaly part
MAE = "mae"
