import union_find
import z3


class Variable:

    def __init__(self, identifier):
        self.identifier = identifier

    def __eq__(self, other):
        return self.identifier == other.identifier


class EquivalenceOp:

    def __init__(self, variable1, variable2):
        self.left = variable1
        self.right = variable2


class Equality(EquivalenceOp):

    def __init__(self, variable1, variable2):
        super().__init__(variable1, variable2)


class Disequality(EquivalenceOp):

    def __init__(self, variable1, variable2):
        super().__init__(variable1, variable2)


class Theory:

    def __init__(self, identifier_map, variables, model=None):

        self.identifier_map = identifier_map
        self.variables = variables
        self.model = model
        self.nodes = dict()
        self.sat = z3.unknown

        for v in self.variables:
            self.nodes[v.identifier] = union_find.UnionNode(v)

    def get_corresponding_nodes(self, varname):

        relation = self.identifier_map[varname]
        left = relation.left
        right = relation.right
        left_node = self.nodes[left.identifier]
        right_node = self.nodes[right.identifier]

        return left_node, right_node

    def clear_relation(self):

        for key in self.nodes:
            self.nodes[key].clear()

    def build_relation(self):

        for var in self.model:
            left_node, right_node = self.get_corresponding_nodes(var.name())

            if z3.is_true(self.model[var]):
                left_node.merge(right_node)

    def check(self, model=None):

        if model is not None:
            self.model = model
            self.clear_relation()

        self.build_relation()

        self.sat = z3.sat

        for var in self.model.decls():
            left_node, right_node = self.get_corresponding_nodes(var.name())

            if not z3.is_true(self.model[var]) and left_node == right_node:
                self.sat = z3.unsat

        return self.sat

    def learn_clause(self):

        if self.sat == z3.unknown or self.sat == z3.sat:
            return None

        else:
            clause = []
            for var in self.model:
                bool_var = z3.Bool(var.name())
                if z3.is_true(self.model[var]):
                    bool_var = z3.Not(bool_var)
                clause += [bool_var]
            return z3.Or(clause)


class Solver:

    def __init__(self, identifier_map, variables):

        self.solver = z3.SolverFor("QF_FD")
        self.theory = Theory(identifier_map, variables)
        self.res = z3.unknown
        self.model = None
        self.assertions = None
        self.formula = None

    def check(self, formula):

        self.solver.add(formula)
        self.formula = formula

        while True:
            sat_res = self.solver.check()
            if z3.unsat == sat_res:
                self.res = sat_res
                break
            elif z3.unknown == sat_res:
                self.res = sat_res
                break
            else:
                theory_res = self.theory.check(self.solver.model())
                if z3.sat == theory_res:
                    self.res = theory_res
                    break
                learnt_clause = self.theory.learn_clause()
                self.solver.add(learnt_clause)
                self.formula = z3.And(self.formula, learnt_clause)

        try:
            self.model = self.solver.model()
        except z3.Z3Exception:
            self.model = None
        self.assertions = self.solver.assertions()
        self.formula = z3.simplify(self.formula)
        return self.res
