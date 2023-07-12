import numpy as np
from pykalman import KalmanFilter
import matplotlib.pyplot as plt


# n = 1000
# time = np.arange(n)
# data = np.sin(0.02 * time) + np.random.randn(n) * 0.1
#
# data[40] = 3
#
# print(data_covariance := np.cov(data))
# print(np.diff(data))
# print(np.cov(np.diff(data)))


def kalman_filter(data , transition_covariance = 0.5):
    data_covariance = np.cov(data)
    kf = KalmanFilter(transition_matrices=[1],
                      observation_matrices=[1],
                      initial_state_mean=data[0],
                      initial_state_covariance=0,
                      observation_covariance=data_covariance,
                      transition_covariance=transition_covariance)

    # filtered_state_means, filtered_state_covariances = kf.filter(data)

    smoothed_state_means, smoothed_state_covariances = kf.smooth(data)
    smoothed_data = smoothed_state_means.flatten()
    return smoothed_data


    # plt.plot(time, data, 'b-', time, smoothed_data, 'r-')
    # plt.legend(['data', 'smoothed data'])
    # plt.show()
