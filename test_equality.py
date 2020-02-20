import unittest
import equivalence as eq
import pysat


class LazyBasicTestCase(unittest.TestCase):

    def test_simple_case(self):
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

        self.assertEqual(pysat.lit_True, s.res, "SAT is incorrect")
        self.assertListEqual([1, 2, 3], s.model, "Model is incorrect")
        self.assertListEqual([[1], [2], [3]], s.formula, "Formula is incorrect")

    def test_unsat_case(self):
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

        self.assertEqual(pysat.lit_False, s.res, "SAT is incorrect")
        self.assertListEqual([], s.model, "Model is incorrect")
        self.assertListEqual([[1], [2], [3], [-4], [-1, -2, -3, 4]], s.formula, "Formula is incorrect")

    def test_case(self):
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

        self.assertEqual(pysat.lit_True, s.res, "SAT is incorrect")
        self.assertListEqual([1, -2, 3, -4, 5, -6], s.model, "Model is incorrect")
        self.assertListEqual(
            [[1],
             [2, -3, -4],
             [5, 4],
             [-2, 6],
             [-1, 2, 3, -4, 5, 6],
             [-1, 2, 3, -4, -5, 6],
             [-1, 2, 3, 4, -5, 6]],
            s.formula, "Formula is incorrect")

    def test_complicated_with_tseitin(self):
        """
        v (x1 == x2 ^ x3 == x4 ^ x5 == x6 ^ x2 != x3 ^ x4 != x5 ^ x1 != x6)
        v (x1 == x2 ^ x3 == x4 ^ x5 == x6 ^ x2 != x3 ^ x4 != x5 ^ x1 != x6 ^ x2 == x4)
        v (x1 == x2 ^ x3 == x4 ^ x5 == x6 ^ x2 != x3 ^ x4 != x5 ^ x1 != x6 ^ x7 == x1 ^ x8 == x7 ^ x8 == x3)
        v (x1 == x2 ^ x3 == x4 ^ x5 == x6 ^ x2 != x3 ^ x4 != x5 ^ x1 != x6 ^ x7 == x1 ^ x8 == x2 ^ x7 != x8)

        v (1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6)
        v (1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 9)
        v (1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 7 ^ 8 ^ 10)
        v (1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 7 ^ 11 ^ -8)

        a1
        a1 -> a2 v a3
        a2 -> 1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6
        a3 -> a4 v a5
        a4 -> 1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 9
        a5 -> a6 v a7
        a6 -> 1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 7 ^ 8 ^ 10
        a7 -> 1 ^ 3 ^ 5 ^ -2 ^ -4 ^ -6 ^ 7 ^ 11 ^ -8

        a1
        -a1 v a2 v a3
        -a2 v 1
        -a2 v 3
        -a2 v 5
        -a2 v -2
        -a2 v -4
        -a2 v -6
        -a3 v a4 v a5
        -a4 v 1
        -a4 v 3
        -a4 v 5
        -a4 v -2
        -a4 v -4
        -a4 v -6
        -a4 v 9
        -a5 v a6 v a7
        -a6 v 1
        -a6 v 3
        -a6 v 5
        -a6 v -2
        -a6 v -4
        -a6 v -6
        -a6 v 7
        -a6 v 8
        -a6 v 10
        -a7 v 1
        -a7 v 3
        -a7 v 5
        -a7 v -2
        -a7 v -4
        -a7 v -6
        -a7 v 7
        -a7 v 11
        -a7 v -8
        """

        x1 = eq.Variable('x1')
        x2 = eq.Variable('x2')
        x3 = eq.Variable('x3')
        x4 = eq.Variable('x4')
        x5 = eq.Variable('x5')
        x6 = eq.Variable('x6')
        x7 = eq.Variable('x7')
        x8 = eq.Variable('x8')

        varb1 = eq.Equality(x1, x2)
        varb2 = eq.Equality(x2, x3)
        varb3 = eq.Equality(x3, x4)
        varb4 = eq.Equality(x4, x5)
        varb5 = eq.Equality(x5, x6)
        varb6 = eq.Equality(x1, x6)
        varb7 = eq.Equality(x7, x1)
        varb8 = eq.Equality(x8, x7)
        varb9 = eq.Equality(x2, x4)
        varb10 = eq.Equality(x8, x3)
        varb11 = eq.Equality(x8, x2)

        identifier_map = \
            {1: varb1, 2: varb2, 3: varb3, 4: varb4, 5: varb5, 6: varb6, 7: varb7, 8: varb8, 9: varb9, 10: varb10, 11: varb11}

        formula = [
            [12],
            [-12, 13, 14],
            [-13, 1],
            [-13, 3],
            [-13, 5],
            [-13, -2],
            [-13, -4],
            [-13, -6],
            [-14, 15, 16],
            [-15, 1],
            [-15, 3],
            [-15, 5],
            [-15, -2],
            [-15, -4],
            [-15, -6],
            [-15, 9],
            [-16, 17, 18],
            [-17, 1],
            [-17, 3],
            [-17, 5],
            [-17, -2],
            [-17, -4],
            [-17, -6],
            [-17, 7],
            [-17, 8],
            [-17, 10],
            [-18, 1],
            [-18, 3],
            [-18, 5],
            [-18, -2],
            [-18, -4],
            [-18, -6],
            [-18, 7],
            [-18, 11],
            [-18, -8],
        ]

        s = eq.Solver(identifier_map, [x1, x2, x3, x4, x5, x6, x7, x8])
        s.check(formula)

        self.assertEqual(pysat.lit_True, s.res, "SAT is incorrect")
        self.assertListEqual(
            [1, -2, 3, -4, 5,
             -6, -7, -8, -9, -10,
             11, 12, 13, -14, -15,
             -16, -17, -18], s.model, "Model is incorrect")
        self.assertListEqual(
            [[12],
             [-12, 13, 14],
             [-13, 1],
             [-13, 3],
             [-13, 5],
             [-13, -2],
             [-13, -4],
             [-13, -6],
             [-14, 15, 16],
             [-15, 1],
             [-15, 3],
             [-15, 5],
             [-15, -2],
             [-15, -4],
             [-15, -6],
             [-15, 9],
             [-16, 17, 18],
             [-17, 1],
             [-17, 3],
             [-17, 5],
             [-17, -2],
             [-17, -4],
             [-17, -6],
             [-17, 7],
             [-17, 8],
             [-17, 10],
             [-18, 1],
             [-18, 3],
             [-18, 5],
             [-18, -2],
             [-18, -4],
             [-18, -6],
             [-18, 7],
             [-18, 11],
             [-18, -8],
             [-1, 2, -3, 4, -5, 6, 7, 8, -9, 10, 11],
             [-1, 2, -3, 4, -5, 6, 7, -8, -9, 10, 11],
             [-1, 2, -3, 4, -5, 6, -7, -8, -9, 10, 11],
             [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10, 11],
             [-1, 2, -3, 4, -5, 6, -7, 8, -9, -10, 11],
             [-1, 2, -3, 4, -5, 6, 7, 8, -9, -10, 11],
             [-1, 2, -3, 4, -5, 6, 7, -8, -9, -10, 11],
             [-1, 2, -3, 4, -5, 6, -7, -8, -9, -10, 11],
             [-1, 2, -3, 4, -5, 6, -7, -8, -9, -10, -11],
             [-1, 2, -3, 4, -5, 6, -7, 8, -9, -10, -11],
             [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10, -11],
             [-1, 2, -3, 4, -5, 6, -7, -8, -9, 10, -11],
             [-1, 2, -3, 4, -5, 6, 7, -8, -9, 10, -11],
             [-1, 2, -3, 4, -5, 6, 7, -8, -9, -10, -11],
             [-1, 2, -3, 4, -5, 6, 7, 8, -9, -10, -11],
             [-1, 2, -3, 4, -5, 6, 7, 8, -9, 10, -11]],
            s.formula, "Formula is incorrect")


if __name__ == '__main__':
    unittest.main()
