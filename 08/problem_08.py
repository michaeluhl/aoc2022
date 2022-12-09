import sys

import numpy as np


data = None

with open(sys.argv[1], "rt") as input_file:
    raw_data = []
    for line in input_file:
        raw_data.append([int(i) for i in line.strip()])
    data = np.asarray(raw_data, dtype=int)

l_max = np.maximum.accumulate(data[1:-1,:-2], axis=1)
r_max = np.maximum.accumulate(data[:,::-1][1:-1,:-2], axis=1)[:,::-1]
t_max = np.maximum.accumulate(data[:-2,1:-1], axis=0)
b_max = np.maximum.accumulate(data[::-1,:][:-2,1:-1], axis=0)[::-1,:]
ss = data[1:-1,1:-1]
viz = (ss <= l_max) & (ss <= r_max) & (ss <= t_max) & (ss <= b_max)

res = np.full(data.shape, True, dtype=bool)
res[1:-1,1:-1] = np.logical_not(viz)
print(res)
print(np.count_nonzero(res))