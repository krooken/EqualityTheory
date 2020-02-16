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

    def __init__(self, identifier_map, variables):

        self.identifier_map = identifier_map
        self.variables = variables
        self.nodes = dict()

        for v in self.variables:
            self.nodes[v.identifier] = union_find.UnionNode(v)

    def get_corresponding_nodes(self, varname):

        relation = self.identifier_map[varname]
        left = relation.left
        right = relation.right
        left_node = self.nodes[left.identifier]
        right_node = self.nodes[right.identifier]

        return left_node, right_node

    def build_relation(self, model):

        for var in model:
            left_node, right_node = self.get_corresponding_nodes(var.name())

            if z3.is_true(model[var]):
                left_node.merge(right_node)

    def check(self, model):

        self.build_relation(model)

        sat = True

        for var in model.decls():
            left_node, right_node = self.get_corresponding_nodes(var.name())

            if not z3.is_true(model[var]) and left_node == right_node:
                sat = False

        return sat
