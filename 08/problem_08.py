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

# end part 1

llen = np.zeros(viz.shape, dtype=int)
rlen = np.zeros_like(llen)
tlen = np.zeros_like(llen)
blen = np.zeros_like(llen)

ss = data[1:-1,1:]
rss = data[1:-1,:-1][:,::-1]
for i in range(viz.shape[1]):
    cansee = ss[:, i, None] <= ss[:,i+1:]
    cansee[:, -1] = True
    llen[:,i] = np.argmax(cansee, axis=1) + 1
    cansee = rss[:, i, None] <= rss[:,i+1:]
    cansee[:, -1] = True
    rlen[:,i] = np.argmax(cansee, axis=1) + 1
rlen = rlen[:,::-1]

ss = data[1:,1:-1]
rss = data[:-1,1:-1][::-1]
for j in range(viz.shape[0]):
    cansee = ss[None, j, :] <= ss[j+1:, :]
    cansee[-1, :] = True
    tlen[j,:] = np.argmax(cansee, axis=0) + 1
    cansee = rss[None, j, :] <= rss[j+1:, :]
    cansee[-1, :] = True
    blen[j,:] = np.argmax(cansee, axis=0) + 1
blen = blen[::-1]
sscore = llen * rlen * tlen * blen
print(sscore.max())