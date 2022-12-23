import sys


class Posn:

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def move(self, modulo=0):
        count = abs(self.value) % modulo if modulo > 0 else abs(self.value)
        for _ in range(count):
            if self.value < 0:
                swap, next = self.prev, self.next
                prev = swap.prev
                self.prev = prev
                prev.next = self
                self.next = swap
                swap.prev = self
                swap.next = next
                next.prev = swap
            else:
                prev, swap = self.prev, self.next
                next = swap.next
                swap.prev = prev
                prev.next = swap
                swap.next = self
                self.prev = swap
                self.next = next
                next.prev = self

    def traverse(self, n):
        p = self
        for _ in range(n):
            p = p.next
        return p

    def __repr__(self):
        return str(self.value)

    def print_ring(self):
        buffer = [self.value]
        n = self
        while n.next != self:
            n = n.next
            buffer.append(n.value)
        print(', '.join([str(v) for v in buffer]))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Program for AoC 2022 Problem 20")
    parser.add_argument('-k', '--key', action="store", type=int, default=1, help="Decryption key (defaults to 1)")
    parser.add_argument('-m', '--mixes', action="store", type=int, default=1, help="Number of times that mixing should be performed.")
    parser.add_argument('input', action="store", type=str, help="Input file to be processed.")
    options = parser.parse_args()

    values = []

    with open(options.input, 'rt') as input_file:
        for line in input_file:
            p = values[-1] if values else None
            n = Posn(int(line.strip()) * options.key, p)
            if p:
                p.next = n
            values.append(n)
        values[0].prev = values[-1]
        values[-1].next = values[0]

    lv = len(values) - 1
    print(f"Shifting mod: {lv}")
    for _ in range(options.mixes):
        for i, v in enumerate(values):
            v.move(lv)

    zero = [v for v in values if v.value == 0][0]
    res = []
    v = zero
    for _ in range(3):
        v = v.traverse(1000)
        res.append(v.value) 

    print(res)
    print("Sum: ", sum(res))