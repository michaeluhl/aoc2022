from ast import literal_eval
from functools import cmp_to_key
import sys


def comp(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return 0 if left == right else -1 if left < right else 1
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            res = comp(l, r)
            if res in (-1, 1):
                return res
        ll, lr = len(left), len(right)
        return 0 if ll == lr else -1 if ll < lr else 1
    if isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]
    return comp(left, right)


count_correct = 0
loop_counter = 1
packets = [[[2]], [[6]]]

with open(sys.argv[1], 'rt') as input_file:
    try:
        while True:
            left = literal_eval(next(input_file))
            right = literal_eval(next(input_file))
            packets.extend([left, right])
            result = comp(left, right) == -1
            print(loop_counter, result)
            count_correct += loop_counter if result else 0
            loop_counter += 1
            _ = next(input_file)
    except StopIteration:
        pass

print(count_correct)

packets.sort(key=cmp_to_key(comp))

div1 = packets.index([[2]]) + 1
div2 = packets.index([[6]]) + 1
print(div1*div2)