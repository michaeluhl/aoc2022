import sys


n_contains = 0
n_overlaps = 0

with open(sys.argv[1], "rt") as input_file:
    for line in input_file:
        r1, _, r2 = line.strip().partition(',')
        r1 = [int(v) for v in r1.partition('-')[::2]]
        r2 = [int(v) for v in r2.partition('-')[::2]]
        if r2[0] >= r1[0] and r2[1] <= r1[1]:
            # r1 contains r2
            n_contains += 1
        elif r1[0] >= r2[0] and r1[1] <= r2[1]:
            # r2 contains r1
            n_contains += 1
        if r2[0] <= r1[1] and r2[1] >= r1[0]:
            n_overlaps += 1
        elif r1[0] <= r2[1] and r1[1] >= r2[0]:
            n_overlaps += 1

print(n_contains)
print(n_overlaps)
