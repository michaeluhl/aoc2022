import sys

fs = {}
dstack = []

small = []
all_dirs = []


with open(sys.argv[1], "rt") as input_file:
    for line in input_file:
        if line.startswith('$ cd '):
            arg = line[5:].strip()
            if arg == "/":
                dstack = [fs]
            elif arg == "..":
                last = dstack.pop(-1)
                dstack[-1]["$total"] += last["$total"]
                all_dirs.append(last["$total"])
                if last["$total"] <= 100000:
                    small.append(last["$total"])
            else:
                dstack.append(dstack[-1][arg])
        elif line.startswith("$ ls"):
            dstack[-1]["$total"] = 0
        else:
            val, name = line.strip().split(' ')
            if val == "dir":
                dstack[-1][name] = {}
            else:
                val = int(val)
                dstack[-1][name] = val
                dstack[-1]["$total"] += val
if len(dstack) > 1:
    last = dstack.pop(-1)
    dstack[-1]["$total"] += last["$total"]
    all_dirs.append(last["$total"])
        
print("Total Size:", fs["$total"])
print("Sum of Small Dirs", sum(small))

total_space = 70000000
required_space = 30000000
free_space = total_space - fs["$total"]
need_space = required_space - free_space
print("Needed Space:", need_space)

candidates = [d for d in all_dirs if d >= need_space]
print(min(candidates))
