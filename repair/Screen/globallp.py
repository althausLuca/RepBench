import numpy as np
import scipy.optimize as opt
import scipy.sparse as sp
from timeit import default_timer as timer

# for time differences = 1 only
# time = None assume values with time differences of 1
def LPconstrainedAE(x, min=2, max=2, time=None, w=1, second=True , truth = None):
    n = len(x)
    A_n_cols = 2 * n
    c = np.ones(A_n_cols)

    if time is None:
        time = np.arange(n)

    A_ub = []
    b_ub = []

    time = np.array(time)
    i = 0
    while True:
        i = i + 1
        diff = time[i:] - time[:-i]
        if np.min(diff) > w:
            break
        else:
            mask = diff <= w
            # i difference  build the full matrix
            A = np.zeros((n - i, n), dtype=np.byte)
            A[np.arange(n - i), np.arange(n - i)] = 1
            A[np.arange(n - i), np.arange(i, n)] = -1

            A = A[mask, :]  # throw away the rows not contained the constraint

            B = np.concatenate((-A, A), axis=1, ) # u then v
            B = np.concatenate((B, -B), axis=0, ) # smin , smax

            xij = (x[:-i] - x[i:])
            b = np.concatenate((xij + max * diff, -xij + min * diff))
            b = b[np.concatenate((mask, mask))]

            A_ub.append(B)
            b_ub.append(b)

    A_ub = np.concatenate(A_ub)
    b_ub= np.concatenate(b_ub)

   

    A_ub = sp.coo_matrix(A_ub)


    A_eq = None
    b_eq = None

    solution = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, np.inf), options={"disp": False})
    uv = solution.x
    x_prime = x + uv[:int(len(uv) / 2)] - uv[int(len(uv) / 2):]

    return x_prime
#print(LPconstrainedAE(np.arange(500),max=0.5))
# example form the paper
# x = np.array([12, 12.5, 13, 10, 15, 15.5])
# t = np.array([1, 2, 3, 5, 7, 8])
#





# start = timer()
# sol = LPconstrainedAE(np.arange(15000), 0.5, 0.5, time=np.arange(15000), w=1 )
# end = timer()
# print(end-start)
# print(sol, "thiiiis")
#
# paper = np.array([12, 12.5, 13, 14, 15, 15.5])


