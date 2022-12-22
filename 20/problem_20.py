import sys


class Posn:

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def move(self):
        for _ in range(abs(self.value)):
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


values = []

with open(sys.argv[1], 'rt') as input_file:
    for line in input_file:
        p = values[-1] if values else None
        n = Posn(int(line.strip()), p)
        if p:
            p.next = n
        values.append(n)
    values[0].prev = values[-1]
    values[-1].next = values[0]

for v in values:
    v.move()

zero = [v for v in values if v.value == 0][0]
res = []
v = zero
for _ in range(3):
    v = v.traverse(1000)
    res.append(v.value) 

print(res)
print("Sum: ", sum(res))