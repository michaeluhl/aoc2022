import math
import operator
import sys


op_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}


class Monkey:

    cdiv = 1

    def __init__(self):
        self.items = []
        self.test_divisor = 1
        self.relax_level = 1
        self.targets = {}
        self.op = lambda x: x
        self.i_ct = 0

    def throw(self, monkeys):
        ttgt = self.targets[True]
        ftgt = self.targets[False]
        self.i_ct += len(self.items)
        for item in self.items:
            item = self.op(item) // self.relax_level
            if item % self.test_divisor == 0:
                monkeys[ttgt].items.append(item % self.cdiv)
            else:
                monkeys[ftgt].items.append(item % self.cdiv)
        del self.items[:]

    @classmethod
    def parse_operation(cls, expr):
        param1, oper, param2 = expr.split(' ')
        if param2 == param1:
            return lambda x: op_map[oper](x, x)
        return lambda x: op_map[oper](x, int(param2))

    @classmethod
    def from_file(cls, file, relax_level=3):
        id = int(next(file).strip().strip(':').partition(' ')[-1])
        items = [int(s.strip()) for s in next(file).strip().partition(':')[-1].split(',')]
        oper = cls.parse_operation(next(file).rpartition('=')[-1].strip())
        divisor = int(next(file).strip().rpartition(' ')[-1])
        ttgt = int(next(file).rpartition(' ')[-1])
        ftgt = int(next(file).rpartition(' ')[-1])
        m = cls()
        m.items = items
        m.op = oper
        m.test_divisor = divisor
        m.targets = {True: ttgt, False: ftgt}
        m.relax_level = relax_level
        return (id, m)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculates monkey business")
    parser.add_argument(
        '-r', "--relax", metavar="r", type=int, default=3,
        help="Relaxation divisor"
    )
    parser.add_argument(
        '-n', "--n-rounds", metavar="N", type=int, default=20,
        help="Number of rounds to evaluate"
    )
    parser.add_argument(
        "input", metavar="FILE", type=str,
        help="File to be read."
    )

    options = parser.parse_args()

    with open(options.input, "rt") as input_file:
        monkeys = []
        try:
            while True:
                monkeys.append(Monkey.from_file(input_file, options.relax))
                next(input_file)
        except StopIteration:
            pass

    monkeys = dict(monkeys)
    cdiv = math.prod([m.test_divisor for m in monkeys.values()])
    Monkey.cdiv = cdiv

    for r in range(options.n_rounds):
        for _, m in sorted(monkeys.items()):
            m.throw(monkeys)

    tops = [v.i_ct for v in sorted(monkeys.values(), key=lambda v: v.i_ct, reverse=True)][:2]
    print(tops[0] * tops[1])
