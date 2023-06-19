import numpy as np
import statistics

from repair.Screen.globallp import LPconstrainedAE

def screen(x, w, smax, smin=None, timestamps=None):
    if timestamps is None:
        timestamps = np.arange(len(x))
    assert len(x) == len(timestamps)

    if smin is None:
        smin = -smax

    t = timestamps
    x_prime = x.copy()
    for k, x_k in enumerate(x):
        X_min, X_max = [], []

        x_min = -np.inf if k == 0 else x_prime[k - 1] + smin * (t[k] - t[k - 1])
        x_max = +np.inf if k == 0 else x_prime[k - 1] + smax * (t[k] - t[k - 1])

        for i in range(k+1,len(x)):
            if t[i] > t[k] + w:
                break
            X_min.append(x[i] + smin * (t[k] - t[i]))
            X_max.append(x[i] + smax * (t[k] - t[i]))


        x_mid = statistics.median(X_min+X_max+ [x_k])

        if x_max < x_mid:
            x_prime[k] = x_max
        elif x_min > x_mid:
            x_prime[k] = x_min
        else:
            x_prime[k] = x_mid
    return x_prime

    # Press the green button in the gutter to run the script.


# filename = "stock10k.data"
# smax = 0.5
# w = 5

# if __name__ == '__main__':
#     T = np.genfromtxt(filename,delimiter=",")
#     print(T)
#     t = T[:, 0]
#     x = T[:, 1]
#     print(t)
#     print(x)
#     x_prime = screen(x,w,smax=smax,timestamps=t)
#     print(x_prime)

# x = [5, 4.5, 6, 11, 5.5, 4, 9, 7,8,8.5,7,6,6.5 ,13 , 4, 5, 5,5.5,6.5,-4,6,  7,]
# smax= 1.5
# w = 2
#
# x_prime = screen(x, w, smax)
# print(x_prime)
# #def LPconstrainedAE(x, min=2, max=2, time=None, w=1, second=True , labels = None , truth = None):
#
# x_lp = LPconstrainedAE(np.array(x),min=smax,max=smax,w=w)
# print(x_lp)
# x_lp
#
# #my_sol = np.array([5, 4.5, 6, 7.5, 5.5, 4, 6, 7])
#
# print(sum(abs(np.array(x)-np.array(x_lp))))
# print(sum(abs(np.array(x)-np.array(x_prime))))
#
# plt.figure(figsize=(10,4))
# plt.plot(x , color= "red" , label="original" ,marker=".")
# plt.plot(x_lp , color= "green" , label="global",marker="x",ls="dashed")
# plt.plot(x_prime, color= "black" , label="local",marker="o",ls="dotted" ,fillstyle='none')
# plt.legend()
#
#
# # plt.savefig("thesisplots/screen.svg")
# plt.show()
#
#
#
#
# ## paper
# x = [5, 4., 13, 10, 15, 15.5]
# t = [1, 2, 3, 5, 7, 8]
# smax = 0.5
# w = 5
#
# x_prime = screen(x, w, smax,timestamps=t)
# print(x_prime)
