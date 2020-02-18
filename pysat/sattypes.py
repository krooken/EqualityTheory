from .satutils import *


# int representations of lits are what the solver reads (-1, +1, -2, +2, ...)
# literals are an internal representation from 0..2n (0=1, 1=-1, 2=2, 3=-2, 4=3, 5=-3, ...)
# This is suitable for array indexing
def int_to_lit(i):
    var = (abs(i) - 1)
    return var_to_lit(var, 1 if i < 0 else 0)


def lit_to_int(lit):
    """ Function for getting external (user) literals indexing (-N..+N) from internal literal indexing (0..2N-1)"""
    var = lit_to_var(lit)
    int_abs = var_to_int(var)
    if lit & 1:  # sign is set
        return - int_abs
    return int_abs


def var_to_int(var):
    return var + 1


# Vars are variable indexes suitable for array indexing (0...n-1)
def var_to_lit(var, var_sign=0):
    return (var << 1) + var_sign


def sign_lit(lit):
    return lit % 2


def not_lit(lit):
    return lit ^ 1


def lit_to_var(lit):
    return lit >> 1


def lit_to_var_sign(lit):
    return lit_to_var(lit), sign_lit(lit)


############################################################################################
class Clause:
    """ Very simple clause wrapper.
    TODO: Needs to add a sorting technique for building the clause"""

    def __init__(self, list_of_literals=None, learnt=False, lbd=None):
        self.literals = array('i')
        self.score = 0.0
        self.learnt = learnt
        self.dll_isSAT = False
        self.dll_size = len(list_of_literals)
        self.var_inc = 0
        self.lbd = lbd
        if list_of_literals is not None:
            self.literals.fromlist(list_of_literals)
        return

    def add_literal(self, lit):
        self.literals.append(lit)

    def remove_literal(self, lit):
        self.literals.remove(lit)

    def contains_literal(self, lit):
        return self.literals.contains(lit)

    def inc_score(self):
        self.score += self.var_inc

    def get_score(self):
        return self.score

    def _calc_abstraction(self):
        """ Computes a simple Bloom filter for the clause. Will be used when we'll preprocess the formulas"""
        bloom_filter = 0
        for i in range(0, len(self.literals)):
            bloom_filter &= (self.literals[i] << (i % 64))

    # We (re)define now some classical Python methods
    def __iter__(self):
        """ Allows to use the iterator from the array import """
        return self.literals.__iter__()

    def __str__(self):
        """ Gets the clause as a list of literals """
        return ",".join(list(map(lambda l: str(lit_to_int(l)), self.literals)))

    def __getitem__(self, x):
        return self.literals[x]

    def __setitem__(self, x, itm):
        self.literals[x] = itm

    def __len__(self):
        return len(self.literals)

    def __lt__(self, other):
        return self.score < other.score
