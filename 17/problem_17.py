from itertools import cycle
import sys

import numpy as np


shapes = [
    np.array([[1, 1, 1, 1]], dtype=np.int8),
    np.array([[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]], dtype=np.int8)[::-1],
    np.array([[0, 0, 1],
              [0, 0, 1],
              [1, 1, 1]], dtype=np.int8)[::-1],
    np.array([[1, 1, 1, 1]], dtype=np.int8).T,
    np.array([[1, 1],
              [1, 1]], dtype=np.int8)
]

with open(sys.argv[1], "rt") as input_file:
    motions = input_file.read().strip()

pit = np.zeros((4*2022, 7), dtype=np.int8)

top = 0

m = 0
lm = len(motions)
for i, s in zip(range(2022), cycle(shapes)):
    sh, sw = s.shape
    sx, sy = 2, top + 3
    while True:
        d = motions[m%lm]
        if d == '<':
            if sx - 1 >= 0:
                tx = sx - 1
                if np.all(s + pit[sy:sy+sh, tx:tx+sw] <= 1):
                    sx = tx
        elif d == '>':
            if sx + 1 + sw <= 7:
                tx = sx + 1
                if np.all(s + pit[sy:sy+sh, tx:tx+sw] <= 1):
                    sx = tx
        m += 1
        ty = sy - 1
        if ty < 0 or np.any(s + pit[ty:ty + sh, sx:sx + sw] > 1):
            break
        sy = ty
    pit[sy:sy+sh, sx:sx+sw] += s
    if sy + sh > top:
        top = sy + sh

print(top)