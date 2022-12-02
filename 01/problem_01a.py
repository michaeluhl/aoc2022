import sys

import numpy as np


mint = lambda a: int(a) if a else 0
with open(sys.argv[1], "rt") as input_file:
    data = np.array([mint(l.strip()) for l in input_file])
sp = np.argwhere(data == 0)
nsp = np.sort(np.vstack([sp, sp+1]).flatten())
totals = np.sort(np.asarray([np.sum(sa) for sa in np.split(data, nsp)[::2]]))[::-1]

print(totals[0], "\n")

print(totals[:3], "\n")

print(np.sum(totals[:3]))
