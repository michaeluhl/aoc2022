import sys
from collections import defaultdict

import numpy as np


CMDS = {
    'L': np.array([-1, 0], dtype=int),
    'R': np.array([1, 0], dtype=int),
    'U': np.array([0, 1], dtype=int),
    'D': np.array([0, -1], dtype=int)
}


def clip(array):
    array[array > 1] = 1
    array[array < -1] = -1
    return array


nodes = [np.array([0, 0], dtype=int) for _ in range(int(sys.argv[1]))]

posns = defaultdict(int)
posns[(0, 0)] += 1

with open(sys.argv[2], "rt") as input_file:
    for line in input_file:
        d, _, c = line.strip().partition(' ')
        step = CMDS[d]
        for i in range(int(c)):
            nodes[0] += step
            for j in range(1, len(nodes)):
                delta = nodes[j - 1] - nodes[j]
                if np.any(np.abs(delta) > 1):
                    nodes[j] += clip(delta)
                    if j == len(nodes) - 1:
                        posns[tuple(nodes[j])] += 1

print(len(posns))
