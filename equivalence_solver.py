import z3
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
    {'b1':  varb1, 'b2': varb2, 'b3': varb3, 'b4': varb4, 'b5': varb5, 'b6': varb6}

b1, b2, b3, b4, b5, b6 = z3.Bools('b1 b2 b3 b4 b5 b6')

s = z3.SolverFor("QF_FD")
s.add(z3.And(b1, z3.Or(b2, z3.Not(b3), z3.Not(b4)), z3.Or(b5, b4), z3.Or(z3.Not(b2), b6)))
print(s.check())
print(s.model())

th = eq.Theory(identifier_map, [x1, x2, x3, x4])
print(th.check(s.model()))


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
    {'b1':  varb1, 'b2': varb2, 'b3': varb3, 'b4': varb4}

b1, b2, b3, b4 = z3.Bools('b1 b2 b3 b4')

s = z3.SolverFor("QF_FD")
s.add(z3.And(b1, b2, b3, z3.Not(b4)))
print(s.check())
print(s.model())

th = eq.Theory(identifier_map, [x1, x2, x3, x4])
print(th.check(s.model()))


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
    {'b1':  varb1, 'b2': varb2, 'b3': varb3}

b1, b2, b3 = z3.Bools('b1 b2 b3')

s = z3.SolverFor("QF_FD")
s.add(z3.And(b1, b2, b3))
print(s.check())
print(s.model())

th = eq.Theory(identifier_map, [x1, x2, x3, x4])
print(th.check(s.model()))
