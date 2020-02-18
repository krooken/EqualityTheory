import union_find
import z3
import pysat


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
        self.sat = pysat.Solver.Constants.lit_Undef

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
            left_node, right_node = self.get_corresponding_nodes(abs(var))

            if var > 0:
                left_node.merge(right_node)

    def check(self, model=None):

        if model is not None:
            self.model = model
            self.clear_relation()

        self.build_relation()

        self.sat = pysat.Solver.Constants.lit_True

        for var in self.model:
            left_node, right_node = self.get_corresponding_nodes(abs(var))

            if not var > 0 and left_node == right_node:
                self.sat = pysat.Solver.Constants.lit_False

        return self.sat

    def learn_clause(self):

        if self.sat == pysat.Solver.Constants.lit_Undef or self.sat == pysat.Solver.Constants.lit_True:
            return None

        else:
            clause = []
            for var in self.model:
                bool_var = -var
                clause += [bool_var]
            return clause


class Solver:

    def __init__(self, identifier_map, variables):

        self.solver = pysat.Solver()
        self.theory = Theory(identifier_map, variables)
        self.res = pysat.Solver.Constants.lit_Undef
        self.model = None
        self.assertions = None
        self.formula = None

    def check(self, formula):

        self.formula = formula

        while True:
            self.solver = pysat.Solver()
            self.solver._config.verbosity = 0
            for clause in self.formula:
                self.solver.addClause(clause)
            self.solver.buildDataStructure()
            sat_res = self.solver.solve(None)
            if pysat.Solver.Constants.lit_False == sat_res:
                self.res = sat_res
                break
            elif pysat.Solver.Constants.lit_Undef == sat_res:
                self.res = sat_res
                break
            else:
                theory_res = self.theory.check(self.solver.finalModel)
                if pysat.Solver.Constants.lit_True == theory_res:
                    self.res = theory_res
                    break
                learnt_clause = self.theory.learn_clause()
                self.formula += [learnt_clause]

        self.model = self.solver.finalModel
        return self.res
