import numpy as np

# Algorithm: LSV (Local Sign Vector). Finds locally optimal sign vector Z, i.e.:
#   Z being locally optimal means: for all Z' sign vectors s.t. Z' is one sign flip away from Z at some index j,
#   we have that ||X^T * Z|| >= ||X^T * Z'||
def local_sign_vector(matrix, Z):
    return local_sign_vector_speed_up(matrix,Z)

    ### loop implementation
    n = len(matrix)
    m = len(matrix[0])
    eps = np.finfo(np.float64).eps

    Z = local_sign_vector_init(matrix, Z)

    # calculate initial product of X^T * Z with the current version of Z
    direction = matrix.T @ Z
    # calculate initial value of ||X^T * Z||
    lastNorm = np.linalg.norm(direction) ** 2 + eps

    flipped = True

    t_loop = time.time()
    while flipped:
        # we terminate the loop if during the last pass we didn't flip a single sign
        flipped = False

        for i in range(0, n):
            signDouble = Z[i] * 2
            gradFlip = 0.0

            # calculate how ||X^T * Z|| would change if we would change the sign at position i
            # change to the values of D = X^T * Z is calculated as D_j_new = D_j - 2 * Z_i * M_ij for all j
            start = time.time()
            for j in range(0, m):
                localMod = direction[j] - signDouble * matrix[i][j]
                gradFlip += localMod * localMod

            # if it results in augmenting ||X^T * Z||
            # flip the sign and replace cached version of X^T * Z and its norm
            if gradFlip > lastNorm:
                flipped = True
                Z[i] = Z[i] * -1
                lastNorm = gradFlip + eps

                for j in range(0, m):
                    direction[j] -= signDouble * matrix[i][j]
                # end for
            # end if
        # end for
    # end while
    return Z


def local_sign_vector_speed_up(matrix, Z):
    Z = Z.copy()
    Z_test = Z.copy()
    eps = np.finfo(np.float64).eps
    Z = local_sign_vector_init_speed_up(matrix, Z)

    #assert np.allclose(Z,local_sign_vector_init(matrix,Z_test))
    # calculate initial product of X^T * Z with the current version of Z
    direction = matrix.T @ Z
    # calculate initial value of ||X^T * Z||
    lastNorm = np.linalg.norm(direction) ** 2 + eps
    flipped = True
    while flipped:
        # we terminate the loop if during the last pass we didn't flip a single sign
        flipped = False
        Z_2_M  = Z[:, None]*2*matrix
        for i, row in enumerate(Z_2_M):
            gradFlip = sum((direction-row)**2)
            if gradFlip > lastNorm:
                flipped = True
                Z[i] = Z[i] * -1
                lastNorm = gradFlip + eps
                direction -= row
    return Z
# end function




def local_sign_vector_init_speed_up(matrix, Z):
    Z = Z.copy()
    direction = matrix[0].copy()
    for i, row in enumerate(matrix):
        if i == 0:
            continue
        gradPlus = sum((direction+row)**2)
        gradMinus = sum((direction-row)**2)

        if gradMinus > gradPlus:
            Z[i] = -1

        direction += Z[i]*row
    return Z

# Auxiliary function for LSV:
#   Z is initialized sequentiually where at each step we see which sign would give a larger increase to ||X^T * Z||
def local_sign_vector_init(matrix, Z):
    Z  = Z.copy()
    n = len(matrix)
    m = len(matrix[0])
    direction = matrix[0].copy()

    for i in range(1, n):
        gradPlus = 0.0
        gradMinus = 0.0

        for j in range(0, m):
            localModPlus = direction[j] + matrix[i][j]
            gradPlus += localModPlus * localModPlus
            localModMinus = direction[j] - matrix[i][j]
            gradMinus += localModMinus * localModMinus

        if gradMinus > gradPlus:
            Z[i] = -1

        for j in range(0, m):
            direction[j] += Z[i] * matrix[i][j]

    return Z




# end function


# initialize sign vector array with default values
def default_SV(n, k):
    # default sign vector is (1, 1, ..., 1)^T
    baseZ = np.array([1.0] * n)
    SV = []

    for i in range(0, k):
        SV.append(baseZ.copy())

    return SV


# end function