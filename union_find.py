class UnionNode:

    def __init__(self, variable):

        self.parent = None
        self.children = []
        self.variable = variable

    def __eq__(self, other):
        if self.parent is None and other.parent is None:
            return self.variable == other.variable
        else:
            return self.find() == other.find()

    def clear(self):
        self.parent = None
        self.children = []

    def neighbors(self):
        return self.children + [self.parent]

    def find(self):

        if self.parent is not None:

            return self.parent.find()

        else:

            return self

    def merge(self, other):

        self_root = self.find()
        other_root = other.find()

        if self_root != other_root:
            other_root.parent = self_root
            self_root.children.append(other_root)
