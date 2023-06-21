import numpy as np
import statistics


def screen(x, w, smax, smin=None, timestamps=None):
    if timestamps is None:
        timestamps = np.arange(len(x))

    if smin is None:
        smin = -smax

    t = timestamps
    x_prime = x.copy()
    for k, x_k in enumerate(x):
        X_min, X_max = [], []

        x_min = -np.inf if k == 0 else x_prime[k - 1] + smin * (t[k] - t[k - 1])
        x_max = +np.inf if k == 0 else x_prime[k - 1] + smax * (t[k] - t[k - 1])

        for i in range(k + 1, len(x)):
            if t[i] > t[k] + w:
                break
            X_min.append(x[i] + smin * (t[k] - t[i]))
            X_max.append(x[i] + smax * (t[k] - t[i]))

        x_mid = statistics.median(X_min + X_max + [x_k])

        if x_max < x_mid:
            x_prime[k] = x_max
        elif x_min > x_mid:
            x_prime[k] = x_min
        else:
            x_prime[k] = x_mid
    return x_prime
