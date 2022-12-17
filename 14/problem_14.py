import sys

import numpy as np


class AbyssError(Exception):
    pass


def draw_grid(grid):
    for row in grid:
        print(''.join(['.' if v == 0 else '#' if v == 3 else 'o' for v in row]))


def fill_walls(walls, x_min, y_min, grid):
    print(f"X Min: {x_min}, Y Min: {y_min}")
    print(f"Grid shape: {grid.shape}")
    for wall in walls:
        for i in range(len(wall) - 1):
            seg = wall[i:i+2]
            delta = np.diff(np.asarray(seg), axis=0)
            delta //= np.abs(delta).max()
            dx, dy = delta[0, :]
            cx, cy = seg[0]
            while True:
                grid[cy - y_min, cx - x_min] = 3
                if (cx, cy) == seg[1]:
                    break
                cx += dx
                cy += dy


def can_move(grid, x, y):
    if y >= grid.shape[0]:
        raise AbyssError()
    if x < 0 or x > grid.shape[1]:
        raise AbyssError()
    if grid[y, x] == 0:
        return True
    return False


def add_sand(x_min, y_min, grid, source_x, source_y=0):
    sx = source_x - x_min
    sy = source_y
    while True:
        for dx, dy in ((0, 1), (-1, 1), (1, 1)):
            tx, ty = sx + dx, sy + dy
            if can_move(grid, tx, ty):
                sx, sy = tx, ty
                break
        else:
            grid[sy, sx] = 1
            return

def make_grid(walls):
    x_min, x_max = walls[0][0][0], walls[0][0][0]
    y_min, y_max = 0, 0
    for wall in walls:
        x_min, y_min = np.vstack([wall, [[x_min, y_min]]]).min(axis=0)
        x_max, y_max = np.vstack([wall, [[x_max, y_max]]]).max(axis=0)
    grid = np.zeros((y_max - y_min + 1, x_max - x_min + 1), dtype=int)
    return (x_min, y_min, grid)


def enbiggen(x_min, y_min, grid):
    n_height = grid.shape[0] + 2
    n_xmin = 500 - n_height
    n_xmax = 500 + n_height
    n_width = n_xmax - n_xmin + 1
    return n_xmin, 0, np.zeros((n_height, n_width), dtype=int)


if __name__ == "__main__":
    walls = []

    with open(sys.argv[1], 'rt') as input_file:
        for line in input_file:
            coords = [tuple([int(i) for i in p.split(',')]) for p in line.strip().split(' -> ')]
            walls.append(coords)

    x_min, y_min, grid = make_grid(walls)
    fill_walls(walls, x_min, y_min, grid)

    i = 0
    try:
        while True:
            add_sand(x_min, y_min, grid, 500)
            i += 1
    except AbyssError:
        pass

    draw_grid(grid)
    print(f"Last Before Overflow: {i}")

    x_min, y_min, ngrid = enbiggen(*make_grid(walls))
    walls.append([(x_min, ngrid.shape[0] - 1), (x_min + ngrid.shape[1] - 1, ngrid.shape[0] - 1)])
    fill_walls(walls, x_min, y_min, ngrid)
    i = 0
    while True:
        add_sand(x_min, y_min, ngrid, 500, -1)
        i += 1
        if ngrid[0, 500 - x_min] > 0:
            break
    draw_grid(ngrid)
    print(f"{i} units of Sand fell")