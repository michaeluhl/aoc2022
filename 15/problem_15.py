import numpy as np


def eval_line(data, radii, line):
    posns = set()
    for row, rad in zip(data, radii):
        diff = np.abs(line - row[1])
        if diff <= rad:
            hrad = rad - diff
            posns.update(range(row[0]-hrad, row[0]+hrad+1))
        if row[3] == line:
            posns.remove(row[2])
    print(len(posns))


def draw_ball(cx, cy, rad, zone):
    ball = set()
    for j, i in zip(range(-rad, 1), range(0, rad+1)):
        points = [
                (cx + i, cy + j), 
                (cx + j, cy + i),
                (cx - i, cy + j),
                (cx - j, cy + i)
        ]
        ball.update([(px, py) for px, py in points if 0 <= px <= zone and 0 <= py <= zone])
    return ball


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A program for AoC 2022, Problem 15")
    parser.add_argument("line", metavar="N", action="store", type=int, help="Line number to evaluate.")
    parser.add_argument("input", metavar="FILE", action="store", type=str, help="File to process.")
    parser.add_argument('-z', '--zone', action="store", default=None, type=int, help="Search zone")
    options = parser.parse_args()

    sensors = []
    beacons = []

    with open(options.input, 'rt') as input_file:
        for line in input_file:
            halves = line.strip().split(':')
            coords = [half.split(',') for half in halves]
            values = [int(c.partition('=')[-1]) for coord in coords for c in coord]
            sensors.append(values[:2])
            beacons.append(values[2:])

    data = np.hstack(
        [
            np.asarray(sensors, dtype=int), 
            np.asarray(beacons, dtype=int)
        ]
    )

    radii = np.abs(data[:, 2:] - data[:, :2]).sum(axis=1)

    xmin = data[:, ::2].min()
    xmax = data[:, ::2].max()
    ymin = data[:, 1::2].min()
    ymax = data[:, 1::2].max()

    print((xmin, ymin), (xmax, ymax))
    eval_line(data, radii, options.line)

    if options.zone:
        candidates = set()
        for (sx, sy), srad in zip(data[:, :2], radii):
            candidates.update(draw_ball(sx, sy, srad + 1, options.zone))
            for (cx, cy), rad in zip(data[:, :2], radii):
                cull = set()
                for tx, ty in candidates:
                    if abs(tx - cx) + abs(ty - cy) <= rad:
                        cull.add((tx, ty))
                candidates -= cull
        print(candidates)
        cx, cy = candidates.pop()
        print(4000000*cx + cy)