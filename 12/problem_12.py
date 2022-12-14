from collections import defaultdict
import sys

import numpy as np


def plot(shape, start, end, prev):
    disp = [['.' for _ in range(shape[1])] for _ in range(shape[0])]
    disp[end[0]][end[1]] = 'E'
    node = end
    while prev[node]:
        next = prev[node]
        if next == start:
            break
        dir = tuple(np.asarray(node) - np.asarray(next))
        if dir == (-1, 0):
            disp[next[0]][next[1]] = '^'
        elif dir == (1, 0):
            disp[next[0]][next[1]] = 'v'
        elif dir == (0, 1):
            disp[next[0]][next[1]] = '>'
        elif dir == (0, -1):
            disp[next[0]][next[1]] = '<'
        node = next
    disp[start[0]][start[1]] = 'S'
    for row in disp:
        print(''.join(row))


def route(start, shape, check_fun, end_fun):
    maxval = np.prod(shape)
    dist = defaultdict(lambda: maxval)
    dist[start] = 0
    prev = defaultdict(lambda: None)
    visited = set()
    nend = None

    q = {start: 0}

    while q:
        node = sorted(q.items(), key=lambda p: p[1])[0][0]
        del q[node]
        visited.add(node)
        for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            v = node[0] + dr, node[1] + dc
            if v in visited or any([i < 0 for i in v]) or any([i >= j for i, j in zip(v, shape)]):
                continue
            if check_fun(node, v):
                alt = dist[node] + 1
                if alt <= dist[v]:
                    dist[v] = alt
                    q[v] = alt
                    prev[v] = node
                if end_fun(v):
                    nend = v
                    break
        else:
            continue
        break
    return nend, prev, dist


start = None
end = None

grid = []

a = ord('a')
z = ord('z')
S = ord('S')
E = ord('E')

with open(sys.argv[1], "rt") as input_file:
    for line in input_file:
        grid.append([ord(c) for c in line.strip()])

print("Input read")

grid = np.asarray(grid, dtype=int)
end = np.unravel_index(grid.argmin(), grid.shape)
grid[end] = z
start = np.unravel_index(grid.argmin(), grid.shape)
grid[start] = a

print("Start and End Found")
print("Grid Size: {}", grid.shape)

(nend, prev, dist) = route(start, 
                           grid.shape, 
                           lambda n, v: grid[v[0], v[1]] - grid[n[0], n[1]] <= 1,
                           lambda e: e == end)


print(dist[end])
plot(grid.shape, start, end, prev)

print(50*'-')

(nend, prev, dist) = route(end, 
                           grid.shape, 
                           lambda n, v: grid[v[0], v[1]] - grid[n[0], n[1]] >= -1,
                           lambda e: grid[e[0], e[1]] == a)

print(dist[nend])
plot(grid.shape, end, nend, prev)
