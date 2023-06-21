# Description of anomaly repair scenarios


## Setup
- We place anomalies randomly after the first 5% of the time series to not start inside an anomaly and the anomalies do not overlap.
- Specifications of lengths exclude point outliers.

## Patterns
N = length of time series 
M = number of time series

K = 1% of N


base:
- N = max; M = max;
- The first time series is contaminated with ~10% anomalies each anomaly has length max(10,K).
- **Is used for training in all scenarios.**

ts_length:
- M = max; N varies between 30% and 100% of the series growing equally at the start and the end, since more information on both sides might give a better repair.
- The first time series is contaminated with ~5% of N max anomalies each anomaly has length max(10,1% of N max) and only the initial 30% of the time series are contaminated.

a_length: 
- N = max; M = max;
- The first time series is contaminated with 3 anomalies and the size is increased from K to 10% of the time series.

a_rate:
- N = max; M = max;
- The first time series is contaminated with 1 to 30 anomalies each anomaly has length K.

a_factor:
- N = max; M = max;
- The first time series is contaminated with 1 anomaly each anomaly has length K and the factor is increased from 1 to 10.
ts_nbr:
- N = max; M  varies from 3 columns to 100% of the columns;
- The first time series is contaminated with 10 anomalies each anomaly has length K.

cts_nbr:
- N = max; M = max
- Number of infected time series from 1 to M  each containing 10 anomalies. Each anomaly has length K and is placed randomly.





