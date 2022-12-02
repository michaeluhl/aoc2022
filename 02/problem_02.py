import sys


with open(sys.argv[1], "rt") as input_file:
    data = [line.strip().partition(" ")[::2] for line in input_file]

data = [(chr(ord(o) + 23), m) for (o, m) in data]

c = "XYZ"
beats = {c[i]: c[i-1] for i in range(3)}

wld = lambda o, m: 6 if beats[m] == o else 3 if m == o else 0
scores = [wld(o, m) + ord(m) - 87 for (o, m) in data]

print(sum(scores))

ldw = lambda o, r: o if r == "Y" else c[c.index(o)-1] if r == "X" else c[(c.index(o)+1) % 3]

throws = [(o, ldw(o, r)) for (o, r) in data]
scores = [wld(o, m) + ord(m) - 87 for (o, m) in throws]

print(data[:10])
print(throws[:10])
print(sum(scores))
