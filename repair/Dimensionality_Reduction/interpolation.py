import numpy as np

def interpolate(matrix, mask):
    n = len(matrix)
    m = len(matrix[0])

    for j in range(0, m):
        mb_start = -1
        prev_value = np.nan
        step = 0  # init

        for i in range(0, n):
            if mask[i][j]:
                # current value is missing - we either start a new block, or we are in the middle of one

                if mb_start == -1:
                    # new missing block
                    mb_start = i
                    mb_end = mb_start + 1

                    while (mb_end < n) and np.isnan(matrix[mb_end][j]):
                        mb_end += 1

                    next_value = np.nan if mb_end == n else matrix[mb_end][j]

                    if mb_start == 0:  # special case #1: block starts with array
                        prev_value = next_value

                    if mb_end == n:  # special case #2: block ends with array
                        next_value = prev_value

                    step = (next_value - prev_value) / (mb_end - mb_start + 1)
                # end if

                matrix[i][j] = prev_value + step * (i - mb_start + 1)
            else:
                # missing block either ended just now or we're traversing normal data
                prev_value = matrix[i][j]
                mb_start = -1
            # end if
        # end for
    # end for

    return matrix