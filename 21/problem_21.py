import operator
import sys


ops = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.floordiv,
    '*': operator.mul,
    '=': operator.eq
}

def val_unkwn(vars, arg1, arg2):
    try:
        val = resolve(vars, arg1)
        u = arg2
    except:
        u = arg1
        val = resolve(vars, arg2)
    return val, u


def solve(vars, value, name):
    try:
        op, arg1, arg2 = vars[name]
        v, u = val_unkwn(vars, arg1, arg2)
        if op == '+':
            return solve(vars, value -v, u)
        elif op == '*':
            return solve(vars, value//v, u)
        elif op == '-' and u == arg2:
            return solve(vars, v - value, u)
        elif op == '-':
            return solve(vars, value+v, u)
        elif op == '/' and u == arg2:
            return solve(vars, v//value, u)
        elif op == '/':
            return solve(vars, value*v, u)
    except TypeError:
        return value


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

variable['humn'] = None
op, arg1, arg2 = variable['root']
v, u = val_unkwn(variable, arg1, arg2)
print(solve(variable, v, u))
