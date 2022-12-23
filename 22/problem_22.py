import re
import sys

import numpy as np


facing = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3
}

class Player:

    def __init__(self, board, r=None, c=None):
        self.board = board
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if (r is not None and c is not None):
            self.r = r
            self.c = c
        else:
            self.r = 1
            self.c = self.board[self.r,:].argmin()
        self.hist = board.copy()
        
    def left(self):
        d = self.directions
        self.directions = d[-1:] + d[:-1]

    def right(self):
        d = self.directions
        self.directions = d[1:] + d[:1]

    def move(self, count):
        dr, dc = self.directions[0]
        for _ in range(count):
            tr, tc = self.r + dr, self.c + dc
            if self.board[tr, tc] == 0:
                self.hist[self.r, self.c] = facing[(dr, dc)] + 4
                self.r, self.c = tr, tc
            elif self.board[tr, tc] == 9:
                print("Found edge...")
                if self.directions[0] == (0, 1):
                    row = self.board[self.r, :]
                    idx = (row == 9).argmin()
                    if row[idx] == 0:
                        self.hist[self.r, self.c] = facing[(dr, dc)] + 4
                        self.c = idx
                if self.directions[0] == (0, -1):
                    row = self.board[self.r, :]
                    idx = (row[::-1] == 9).argmin()
                    idx = row.shape[0] - (idx + 1)
                    if row[idx] == 0:
                        self.hist[self.r, self.c] = facing[(dr, dc)] + 4
                        self.c = idx
                if self.directions[0] == (1, 0):
                    col = self.board[:, self.c]
                    idx = (col == 9).argmin()
                    if col[idx] == 0:
                        self.hist[self.r, self.c] = facing[(dr, dc)] + 4
                        self.r = idx
                if self.directions[0] == (-1, 0):
                    col = self.board[:, self.c]
                    idx = (col[::-1] == 9).argmin()
                    idx = col.shape[0] - (idx + 1)
                    if col[idx] == 0:
                        self.hist[self.r, self.c] = facing[(dr, dc)] + 4
                        self.r = idx

    def do(self, inst):
        if isinstance(inst, int):
            self.move(inst)
        elif inst in ('L', 'R'):
            if inst == 'L':
                self.left()
            if inst == 'R':
                self.right()


board = []
maxwidth = 0
instr = None

with open(sys.argv[1], 'rt') as input_file:
    for line in input_file:
        if line[0].isalnum():
            instr = line.strip()
        else:
            line = line.rstrip()
            if line:
                maxwidth = max(maxwidth, len(line))
                board.append(line)

nboard = np.full((len(board)+2, maxwidth+2), 9, dtype=int)
for j, row in enumerate(board, start=1):
    nrow = np.asarray(['9' if c == ' ' else 0 if c == '.' else 8 for c in row])
    nboard[j, 1:nrow.shape[0]+1] = nrow

p = Player(nboard)
inst_l = re.findall(r'(\d+|L|R)', instr)
inst_l = [i if i.isalpha() else int(i) for i in inst_l]

for inst in inst_l:
    p.do(inst)

print(p.r, p.c, facing[p.directions[0]])
print(1000 * p.r + 4 * p.c + facing[p.directions[0]])

# m = {9:' ', 8:'#', 0:'.', 4:'>', 5:'v', 6:'<', 7:'^'}
# for row in p.hist:
#     print(''.join([m[v] for v in row]))
