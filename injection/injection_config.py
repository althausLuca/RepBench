##### Anomalies
AMPLITUDE_SHIFT = "shift"
DISTORTION = "distortion"
POINT_OUTLIER = "outlier"


ANOMALY_TYPES = (AMPLITUDE_SHIFT,
                 DISTORTION,
                 POINT_OUTLIER)

## default values
BASE_FACTORS = {AMPLITUDE_SHIFT: 2,
                DISTORTION: 2,
                POINT_OUTLIER: 3}

BASE_PERCENTAGES = {AMPLITUDE_SHIFT: 5,
                    DISTORTION: 5,
                    POINT_OUTLIER: 2
                    }

DEFAULT_LENGTH = 30  # ignored by point outliers



### IMR labels
label_seed = 100
label_rate = 0.2
anomstartlabelrate = 0.2
