import sys

import numpy as np


def flood(fld):
    q = {(0,0,0)}
    v = lambda fi: all(0 <= i < s for i, s in zip(fi, fld.shape))
    while q:
        i, j, k = q.pop()
        val = fld[i, j, k]
        for di, dj, dk in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            fi = (i+di, j+dj, k+dk)
            if v(fi) and fld[fi] == val:
                q.add(fi)
        fld[i, j, k] = 1
    return fld
    

if __name__ == "__main__":

    indices = []
    with open(sys.argv[1], 'rt') as input_file:
        for line in input_file:
            indices.append([int(v) for v in line.strip().split(',')])
    indices = np.asarray(indices, dtype=int)
    xmax, ymax, zmax = indices.max(axis=0)

    grid = np.zeros((xmax+3, ymax+3, zmax+3), dtype=int)
    grid[indices[:, 0]+1, indices[:, 1]+1, indices[:, 2]+1] = 1
    faces = np.count_nonzero(np.diff(grid, axis=0)) + \
            np.count_nonzero(np.diff(grid, axis=1)) + \
            np.count_nonzero(np.diff(grid, axis=2))

    print("Non-zero elements: ", np.count_nonzero(grid))
    print("Face count: ", faces)

    filled = flood(grid.copy())
    filled[filled == 1] = -1
    filled[filled == 0] = 1
    filled[filled == -1] = 0
    grid += filled

    faces = np.count_nonzero(np.diff(grid, axis=0)) + \
            np.count_nonzero(np.diff(grid, axis=1)) + \
            np.count_nonzero(np.diff(grid, axis=2))
    print("Face count (internal voids excluded): ", faces)
