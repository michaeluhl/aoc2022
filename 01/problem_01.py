import sys

groups = []
with open(sys.argv[1], 'rt') as input_file:
    group = []
    for line in input_file:
        line = line.strip()
        if line == "" and group:
            groups.append(group)
            group = []
        else:
            group.append(int(line))
    if group:
        groups.append(group)

totals = [sum(g) for g in groups]
print(max(totals))

print("")
stotals = sorted(totals, reverse=True)
for t in stotals[:3]:
    print(t)

print("")
print(sum(stotals[:3]))
