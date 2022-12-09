import sys

import numpy as np


data = None

with open(sys.argv[1], "rt") as input_file:
    raw_data = []
    for line in input_file:
        raw_data.append([int(i) for i in line.strip()])
    data = np.asarray(raw_data, dtype=int)

left = data[1:-1,1:-1] <= np.maximum.accumulate(data[1:-1,:-2], axis=1)
datav = data[:,::-1]
right = (datav[1:-1,1:-1] <= np.maximum.accumulate(datav[1:-1,:-2], axis=1))[:,::-1]
top = data[1:-1,1:-1] <= np.maximum.accumulate(data[:-2,1:-1], axis=0)
datav = data[::-1,:]
bot = (datav[1:-1,1:-1] <= np.maximum.accumulate(datav[:-2,1:-1], axis=0))[::-1,:]

viz = (left & right & top & bot)

res = np.full(data.shape, True, dtype=bool)
res[1:-1,1:-1] = np.logical_not(viz)
print(res)
print(np.count_nonzero(res))