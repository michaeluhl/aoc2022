class Elf:

    checks = {
        (0, 1): ((-1, 1), (0, 1), (1, 1)),
        (0, -1): ((-1, -1), (0, -1), (1, -1)),
        (-1, 0): ((-1, -1), (-1, 0), (-1, 1)),
        (1, 0): ((1, -1), (1, 0), (1, 1))
    }
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.px, self.py = None, None

    def propose(self, elves):
        x, y = self.x, self.y
        lc = [
            [
                (x + tx, y + ty) in elves for tx, ty in self.checks[d]
            ] 
            for d in type(self).directions
        ]
        if all([not any(dc) for dc in lc]):
            return None, None
        for d, dc in zip(type(self).directions, lc):
            if not any(dc):
                dx, dy = d
                self.px, self.py = x+dx, y+dy
                return self.px, self.py
        return None, None

    def clear(self):
        self.px, self.py = None, None

    def move(self):
        if self.px is not None and self.py is not None:
            self.x, self.y = self.px, self.py
            self.px, self.py = None, None
        return self.x, self.y

    @classmethod
    def rotate_search(cls):
        d = cls.directions
        cls.directions = d[1:] + d[:1]


def load_elves(filename):
    elves = []
    with open(filename, 'rt') as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line):
                if c == '#':
                    elves.append(Elf(x, -1*y))
    return elves


def draw(coords, quiet):
    x, y = zip(*coords)
    mnx, mxx = min(x), max(x)
    mny, mxy = min(y), max(y)
    if not quiet:
        display = [['.' for _ in range(mxx - mnx + 1)] for _ in range(mxy - mny + 1)]
        for cx, cy in coords:
            display[cy - mny][cx - mnx] = '#'
        for row in display[::-1]:
            print(''.join(row))
    return (mxx - mnx + 1, mxy - mny + 1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Program for AoC Day 23")
    parser.add_argument(
        '-n', '--num-rounds', action="store", type=int, default=10,
        help="Number of rounds to simulate."
    )
    parser.add_argument(
        '-q', '--quiet', action="store_true", help="Do not draw the field"
    )
    parser.add_argument(
        'input', action="store", type=str, help="File to process"
    )
    options = parser.parse_args()

    elves = load_elves(options.input)
    coords = {(e.x, e.y) for e in elves}
    width, height = draw(coords, options.quiet)
    print('')
    sat = True
    for i in range(options.num_rounds):
        sat = True
        proposals = {}
        for elf in elves:
            proposals.setdefault(elf.propose(coords), []).append(elf)
        for _, pes in proposals.items():
            if len(pes) == 1:
                e = pes.pop()
                e.move()
                sat = False
            else:
                for e in pes:
                    e.clear()
        Elf.rotate_search()
        coords = {(e.x, e.y) for e in elves}
        print(f"End Round {i+1}")
        width, height = draw(coords, options.quiet)
        if sat:
            break
    print(f"Width: {width}, Height: {height}")
    print(f"N-Elves: {len(elves)}")
    print(f"Free Space: ", width*height - len(elves))
    if sat:
        print(f"First round with satisifed elves: {i+1}")
