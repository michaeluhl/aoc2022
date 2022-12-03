import sys

total_priority = 0
group_priority = 0
group_set = None

def priority(chars):
    return [ord(c) - 96 if c.islower() else ord(c) - 38 for c in chars]


with open(sys.argv[1], "rt") as input_file:
    for i, line in enumerate(input_file):
        line = line.strip()
        if i % 3 == 0:
            if group_set:
                group_priority += sum(priority(group_set))
            group_set = set(line)
        group_set &= set(line)
        split_pt = len(line)//2
        comp1, comp2 = line[:split_pt], line[split_pt:]
        common = set(comp1) & set(comp2)
        total_priority += sum(priority(common))
    if group_set:
        group_priority += sum(priority(group_set))

print(total_priority)
print(group_priority)
