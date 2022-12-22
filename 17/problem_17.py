from collections import Counter
from itertools import chain, cycle
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


class Window:

    def __init__(self, width, height):
        self.d = np.zeros((height, width), dtype=np.int8)
        self.bot = 0

    def scroll(self):
        self.d = np.roll(self.d, self.d.shape[0]//2, axis=0)
        self.d[-self.d.shape[0]//2:] = 0
        self.bot += self.d.shape[0]//2

    def r(self, y):
        return y - self.bot


def simulate(steps, motions):
    w = Window(7, 8000)

    top = 0
    history = []

    m, lm = 0, len(motions)
    for i, s in zip(range(steps), cycle(shapes)):
        sh, sw = s.shape
        sx, sy = 2, top + 3
        while True:
            d = motions[m%lm]
            if d == '<':
                if sx - 1 >= 0:
                    tx = sx - 1
                    if np.all(s + w.d[w.r(sy):w.r(sy+sh), tx:tx+sw] <= 1):
                        sx = tx
            elif d == '>':
                if sx + 1 + sw <= 7:
                    tx = sx + 1
                    if np.all(s + w.d[w.r(sy):w.r(sy+sh), tx:tx+sw] <= 1):
                        sx = tx
            m += 1
            ty = sy - 1
            if ty < w.bot or np.any(s + w.d[w.r(ty):w.r(ty+sh), sx:sx + sw] > 1):
                break
            sy = ty
        w.d[w.r(sy):w.r(sy+sh), sx:sx+sw] += s
        if sy + sh > top:
            top = sy + sh
        prof = np.argmax(w.d[::-1].astype(bool), axis=0)
        prof -= prof.min()
        history.append((i%5, d, tuple(prof), top))
        if top - w.bot > 3 * w.d.shape[0] // 4:
            w.scroll()
    return history


def find_start_period_and_delta(history):
    repeats = Counter([r[:-1] for r in history])
    repeat_keys = {k for k, v in repeats.items() if v > 1}
    key_idxs = {}
    for i, r in enumerate(history):
        if r[:-1] in repeat_keys:
            key_idxs.setdefault(r[:-1], []).append(i)
    key_freqs = {k: np.diff(kidxs) for k, kidxs in key_idxs.items()}
    freq = max((c:=Counter(chain(*key_freqs.values()))), key=c.get)
    key_idxs = {k: idxs for k, idxs in key_idxs.items() if freq in key_freqs[k]}
    start = min([min(idxs) for idxs in key_idxs.values()])
    start_height = history[start - 1][-1]
    idxs = [i for i, r in enumerate(history) if r[:-1] == history[start][:-1]]
    period = np.diff(idxs)[0]
    deltas = [h[-1] - history[start-1][-1] for h in history[start-1:start + period]]
    return start, start_height, period, deltas


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Program for AoC 2022, Problem 17")
    parser.add_argument(
        "-n", "--num-rocks", action="store", type=int,
        default=2022, help="Number of rocks to simulate..."
    )
    parser.add_argument(
        "input", type=str, action="store",
        help="File to read for input."
    )

    options = parser.parse_args()
    with open(options.input, "rt") as input_file:
        motions = input_file.read().strip()

    print(f"Number of motions: {len(motions)}")
    sim_period = len(motions)*len(shapes)
    sim_period = sim_period if options.num_rocks > sim_period else options.num_rocks        

    history = simulate(sim_period, motions)
    if sim_period == options.num_rocks:
        print(history[-1][-1])
        sys.exit(0)

    # for i, row in enumerate(history[:500]):
    #     print(f"{i:03d}: ", row)


    start, start_height, period, deltas = find_start_period_and_delta(history)
    print(start, start_height, period, deltas[-1])

    periods = (options.num_rocks - (start))// period
    rem = (options.num_rocks - (start)) % period
    height = start_height + periods*deltas[-1] + deltas[rem]
    print(height)