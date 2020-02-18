import equivalence as eq

"""
(x1 == x4) ^ (x1 == x2 v x1 != x3 v x2 != x4) ^ (x3 == x4 v x2 == x4) ^ (x1 != x2 v x2 == x3)
b1 ^ (b2 v -b3 v -b4) ^ (b5 v b4) ^ (-b2 v b6)
"""

x1 = eq.Variable('x1')
x2 = eq.Variable('x2')
x3 = eq.Variable('x3')
x4 = eq.Variable('x4')

varb1 = eq.Equality(x1, x4)
varb2 = eq.Equality(x1, x2)
varb3 = eq.Equality(x1, x3)
varb4 = eq.Equality(x2, x4)
varb5 = eq.Equality(x3, x4)
varb6 = eq.Equality(x2, x3)

identifier_map = \
    {1: varb1, 2: varb2, 3: varb3, 4: varb4, 5: varb5, 6: varb6}

formula = [
    [1],
    [2, -3, -4],
    [5, 4],
    [-2, 6]
]

s = eq.Solver(identifier_map, [x1, x2, x3, x4])
s.check(formula)
print(s.res)
print(s.model)
print(s.assertions)
print(s.formula)

"""
x1 == x2 ^ x2 == x3 ^ x3 == x4 ^ x4 != x1
b1 ^ b2 ^ b3 ^ -b4
"""

x1 = eq.Variable('x1')
x2 = eq.Variable('x2')
x3 = eq.Variable('x3')
x4 = eq.Variable('x4')

varb1 = eq.Equality(x1, x2)
varb2 = eq.Equality(x2, x3)
varb3 = eq.Equality(x3, x4)
varb4 = eq.Equality(x4, x1)

identifier_map = \
    {1: varb1, 2: varb2, 3: varb3, 4: varb4}

formula = [
    [1],
    [2],
    [3],
    [-4]
]

s = eq.Solver(identifier_map, [x1, x2, x3, x4])
s.check(formula)
print(s.res)
print(s.model)
print(s.assertions)
print(s.formula)

"""
x1 == x2 ^ x2 == x3 ^ x3 == x4
b1 ^ b2 ^ b3
"""

x1 = eq.Variable('x1')
x2 = eq.Variable('x2')
x3 = eq.Variable('x3')
x4 = eq.Variable('x4')

varb1 = eq.Equality(x1, x2)
varb2 = eq.Equality(x2, x3)
varb3 = eq.Equality(x3, x4)

identifier_map = \
    {1: varb1, 2: varb2, 3: varb3}

formula = [
    [1],
    [2],
    [3]
]

s = eq.Solver(identifier_map, [x1, x2, x3, x4])
s.check(formula)
print(s.res)
print(s.model)
print(s.assertions)
print(s.formula)
