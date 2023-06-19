import numpy as np
from numpy.linalg import LinAlgError


def imr(x, y_0, labels, tau=0.1, p=1, k=20000):
    if len(labels) == len(x):
        labels = np.arange(len(labels))[labels]
    y_k = x.copy()
    y_k[labels] = y_0[labels]

    n = len(x)
    iterations = 0
    # print(k)
    for iter_counter in range(k):
        y_k_x_diff = y_k - x
        V_k = y_k_x_diff[p:]
        Z_k = np.zeros((n - p, p))
        for i in range(0, p):
            Z_k[:, i] = y_k_x_diff[i:n - p + i]

        phi = np.linalg.inv(Z_k.T.dot(Z_k)).dot(Z_k.T).dot(V_k)

        ## candidate generation
        y_hat = Z_k.dot(phi)+x[p:] ## predicted values (shifted)
        candidates = y_hat-y_k[p:]

        candidates[ np.logical_or(np.abs(candidates)<tau , candidates == 0) ] = np.inf # bigger than tau
        candidates[labels-p] = np.inf # not considering labeled
        if not any(candidates != np.inf):
            #print("imr iteration stopped at" ,iter_counter)
            break

        ## select smallest index
        index = np.argmin(candidates)
        repair_value = y_hat[index]
        y_k[index+p] = repair_value # +p to get the original index

    return { "repair" : y_k , "iterations"  : iterations , "max_iterations" :k , "tau" : tau , "p" : p , "labels" : labels}

# def imr2(x, y_0, labels, tau=0.1, p=1, k=20000):
#     if len(labels) == len(x):
#         labels = np.arange(len(labels))[labels]
#     y_k = x.copy()
#     y_k[labels] = y_0[labels]
#
#     n = len(x)
#     iterations = 0
#     for iter_counter in range(k):
#         y_k_x_diff = y_k - x
#         V_k = y_k_x_diff[p:]
#         Z_k = np.zeros((n - p, p))
#         for i in range(0, p):
#             Z_k[:, i] = y_k_x_diff[i:n - p + i]
#
#         non_zero_vk = ~np.all(Z_k == 0, axis=1)
#         Z_k_cutted , V_k_cutted = Z_k[non_zero_vk,:] , V_k[non_zero_vk]
#         phi = np.linalg.inv(Z_k_cutted.T.dot(Z_k_cutted)).dot(Z_k_cutted.T).dot(V_k_cutted)
#         ## candidate generation
#         y_hat = Z_k.dot(phi)+x[p:] ## predicted values (shifted)
#         candidates = y_hat-y_k[p:]
#
#         candidates[ np.logical_or(np.abs(candidates)<tau , candidates == 0) ] = np.inf # bigger than tau
#         candidates[labels-p] = np.inf # not considering labeled
#         if not any(candidates != np.inf):
#             #print("imr iteration stopped at" ,iter_counter)
#             break
#
#         ## select smallest index
#         index = np.argmin(candidates)
#         repair_value = y_hat[index]
#         y_k[index+p] = repair_value # +p to get the original index
#
#     return { "repair" : y_k , "iterations"  : iterations , "max_iterations" :k , "tau" : tau , "p" : p , "labels" : labels}
#
