import operator
import sys


ops = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.floordiv,
    '*': operator.mul,
    '=': operator.eq
}


def resolve(vars, name):
    expr = vars[name]
    if isinstance(expr, int):
        return expr
    op, arg1, arg2 = expr
    arg1 = resolve(vars, arg1)
    arg2 = resolve(vars, arg2)
    return ops[op](arg1, arg2)


variable = {}

with open(sys.argv[1], 'rt') as input_file:
    for line in input_file:
        name, _, expr = line.partition(':')
        tokens = expr.strip().split(' ')
        if len(tokens) == 1:
            variable[name] = int(tokens[0])
        else:
            variable[name] = (tokens[1], tokens[0], tokens[2])

print(resolve(variable, 'root'))
