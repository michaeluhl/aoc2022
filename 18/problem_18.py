import sys

import numpy as np


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
