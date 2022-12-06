import sys

import numpy as np


data = []
cmds = []
with open(sys.argv[1], "rt") as input_file:
    for i, line in enumerate(input_file):
        if line.strip() == "":
            break
        for j, c in enumerate(line.rstrip()):
            if c.isalpha():
                data.append((i, j, c))
            if c.isdigit():
                data.append((-1, j, c))
    for line in input_file:
        cmds.append([int(v)  for v in line.split()[1::2]])

col = {j: int(c) for i, j, c in data if i == -1}
print(col)

data.sort(key=lambda v: v[0], reverse=True)

stacks = {}
for i, j, c in data:
    if i == -1:
        continue
    stacks.setdefault(col[j], []).append(c)

for n, s in sorted(stacks.items()):
    print(n, s)

for num, start, end in cmds:
    crates = stacks[start][-1*num:]
    del stacks[start][-1*num:]
    if not len(sys.argv) > 2:
        crates = crates[::-1]
    stacks[end].extend(crates)

for n, s in sorted(stacks.items()):
    print(n, s)

print(''.join([s[-1] for _, s in sorted(stacks.items())]))
