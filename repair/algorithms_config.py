from collections import defaultdict

## algorithms

"""
Names of the algorithms
If you change any name make sure to modify parameters.toml accordingly
"""
IMR = "IMR"
SCREEN = "SCREEN"
RPCA = "RPCA"
Robust_PCA = RPCA
CDREP = "CDREP"
SCR = "SCR"
KalmanFilter = "KFilter"

WindowRPCA = "wrpca"
SCREEN_l = "screen_5_95"
SCREEN_l2 = "screen_10_90"

SPEEDandAcceleration = "SCREEN*"
ALGORITHM_TYPES = (IMR,SCREEN,RPCA,CDREP,SPEEDandAcceleration,SCR,KalmanFilter)



#black is used for the truth, and red for anomalies
ALGORITHM_COLORS = {IMR : "blue" , SCREEN : "purple" , RPCA : "green" , CDREP : "orange", KalmanFilter : "brown"  , SPEEDandAcceleration : "pink"}
ALGORITHM_COLORS = defaultdict(lambda: 'cyan', ALGORITHM_COLORS )


## metrics
RMSE = "rmse"
PARTIAL_RMSE = "rmse_partial" #only on the anomaly part
MAE = "mae"
