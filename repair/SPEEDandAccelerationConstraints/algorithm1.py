import numpy as np


def algorithm1(x: np.array, smin=-1, smax=1, amin=-1, amax=1, w=5):
    t = np.arange(len(x))
    x_prime = np.zeros_like(x)  # repair
    for k, x_k in enumerate(x):
        X_min, X_max = set(), set()

        """
        compute x_min_k and x_max_k with formula 16
         x_min_k = x_min_k_k-1 =  max(x_min_k,k-1,s | x_min_k,k-1,a )
         x_min_k,k-1,a = (amin * (t_k - t_k-1) + (x_prime_k-1 - x_prime_k-2)/(t_k-1 - t_k-2))/(t_k - t_k-1)+x_prime_k-1
         x_min_k,k-1,s = x_prime_k-1 + smin * (t_k - t_k-1)
         
          x_max_k = x_max_k,k-1 =  min(x_max_k,k-1,s | x_max_k,k-1,a )
          x_max_k,k-1,a = (amax * (t_k - t_k-1) + (x_prime_k-1 - x_prime_k-2)/(t_k-1 - t_k-2))/(t_k - t_k-1)+x_prime_k-1
          x_max_k,k-1,s = x_prime_k-1 + smax * (t_k - t_k-1)
         """
        if k == 0:  # I assume the first point is initalized to be flexible
            x_min_k = -np.inf
            x_max_k = np.inf
        else:
            xmin_k_a = (amin * (t[k] - t[k - 1]) + (x_prime[k - 1] - x_prime[k - 2]) / (t[k - 1] - t[k - 2])) / \
                       (t[k] - t[k - 1]) + x_prime[k - 1]
            xmin_k_s = x_prime[k - 1] + smin * (t[k] - t[k - 1])
            x_min_k = max(xmin_k_a, xmin_k_s)

            xmax_k_a = (amax * (t[k] - t[k - 1]) + (x_prime[k - 1] - x_prime[k - 2]) / (t[k - 1] - t[k - 2])) / \
                       (t[k] - t[k - 1]) + x_prime[k - 1]
            xmax_k_s = x_prime[k - 1] + smax * (t[k] - t[k - 1])
            x_max_k = min(xmax_k_s, xmax_k_a)

        for i in range(k +1, len(x)):
            if t[i] - t[k] > w:
                break
            """
            compute zmin_k_i_a and zmax_k_i_a with formula 35 and 36
            z_max_k_i_a = (x_prime_k-1*(t_i - t_k) -  (amax*(t_i - t_k)**2 -x_i )*(t_k - t_k-1))/(t_i - t_k-1)
            z_min_k_i_a = (x_prime_k-1*(t_i - t_k) -  (amin*(t_i - t_k)**2 -x_i )*(t_k - t_k-1))/(t_i - t_k-1)
            """
            # we assume time stamps are ordered i dont see the point of this coniditon here
            if k == 0:
                z_max_k_i_a = np.inf
                z_min_k_i_a = -np.inf
            else:
                z_max_k_i_a = (x_prime[k - 1] * (t[i] - t[k]) - (amax * (t[i] - t[k]) ** 2 - x[i]) * (t[k] - t[k - 1]))/ \
                            (t[i] - t[k - 1])
                z_min_k_i_a = (x_prime[k - 1] * (t[i] - t[k]) - (amin * (t[i] - t[k]) ** 2 - x[i]) * (t[k] - t[k - 1]))/ \
                            (t[i] - t[k - 1])
            """
            compute zmin_k_i_s and zmax_k_i_s with formula 34 and 36
            z_max_k_i_a = (x_prime_k-1*(t_i - t_k) -  (amax*(t_i - t_k)**2 -x_i )*(t_k - t_k-1))/(t_i - t_k-1)
            z_min_k_i_a = (x_prime_k-1*(t_i - t_k) -  (amin*(t_i - t_k)**2 -x_i )*(t_k - t_k-1))/(t_i - t_k-1)
            """
            if k == 0:
                z_max_k_i_s = np.inf
                z_min_k_i_s = -np.inf
            else:
                z_max_k_i_s = x[i] - smax * (t[i] - t[k])
                z_min_k_i_s = x[i] - smin * (t[i] - t[k])

            X_min.add(min(z_min_k_i_a, z_min_k_i_s)) # not sure if this should be a max in the paper it is a min
            X_max.add(max(z_max_k_i_a, z_max_k_i_s)) # not sure if this should be a min in the paper it is a max
            print(k,z_min_k_i_a, z_min_k_i_s)
        """
        compute x_mid_k with formula 41
        xmid_k = median(X_min U X_max U {x_k))
        """
        x_mid_k = np.median(list(X_min.union(X_max).union({x[k]})))
        # print(list(X_min.union(X_max).union({x[k]})), x_mid_k)
        """
        compute x_prime_k (repair) with formula 41
        xmid_k = median(X_min U X_max U {x_k)) 46
        """
        if x_max_k < x_mid_k:
            x_prime[k] = x_max_k
        elif x_min_k > x_mid_k:
            x_prime[k] = x_min_k
        else:
            x_prime[k] = x_mid_k

    return x_prime



"""
Example 3.9
"""""
x = np.array([0, 0.5, 2.5, 6.9, 6])
w = 2
# from example 3.7
smin = -5
smax = 5
amax = 1
amin = -1

"""
should results in  {0, 0.5, 2, 4.5, 6}
"""

repair = algorithm1(x, smin, smax,amin, amax,w)
print(repair)



"""
Example plot aproximation
"""""
x = np.array([1.25, 1.2, 1.35, 1.25, 1.2,1.25,1.35,1.25,1.25,1.2,1.3,1.35,1.2,1.4,2.5 ,1.3,1.32
              ,1.27,1.2,1.35,1.22,0,0,0,0,1.24,1.22,1.26,1.22,1.2,1.15,1.15,1.15,1.15,1.15,1.15])
# from example 3.7
smin = -0.151
smax = 0.151
amax =  0.1
amin =  -0.1
w = 1
repair = algorithm1(x, smin, smax,amin, amax,w)

import matplotlib.pyplot as plt
plt.plot(x, label="original")
plt.plot(repair, label="repaired")
plt.legend()
plt.show()