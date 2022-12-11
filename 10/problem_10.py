import sys


inst_times = {
    'addx': 2,
    'noop': 1
}

sig_strength = []

program = []
with open(sys.argv[1], "rt") as input_file:
    for line in input_file:
        program.append(line.strip().partition(" ")[::2])

ip = 0
tc = 0
ic = 0
inst, inst_arg = None, None
reg = {'X': 1}

crt = [[]]

try:
    while True:
        tc += 1
        if ic == 0:
            inst, inst_arg = program[ip]
            ic = inst_times[inst]
        ic -= 1
        if (tc - 20) % 40 == 0:
            sig_strength.append(tc * reg['X'])
        pos = (tc - 1) % 40
        if (reg['X'] - 1) <= pos <= (reg['X'] + 1):
            crt[-1].append("#")
        else:
            crt[-1].append(".")
        if len(crt[-1]) == 40:
            crt.append([])
        if ic == 0:
            if inst == 'addx':
                reg['X'] += int(inst_arg)
            inst, inst_arg = None, None
            ip += 1
except IndexError:
    pass

print(sig_strength)
print(sum(sig_strength))

for row in crt:
    print(''.join(row))
