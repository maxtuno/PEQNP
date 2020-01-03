import sys

from peqnp import *

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('This generate the first 10 magic squares')
        print('Usage   : python3 magic.py')
        print('Example : python3 magic.py')
        exit(0)

    n = 3
    for _ in range(10):
        # Ensure the problem can be represented
        engine((n ** 3).bit_length())

        # The value that all columns, rows and diagonal sum
        c = integer()

        # A matrix of integers of dimension nxn
        xs = matrix(dimensions=(n, n))

        # All elements are nonzero
        apply_single(flatten(xs), lambda x: x > 0)

        # All elements are different (is magic square)
        apply_dual(flatten(xs), lambda a, b: a != b)

        # All columns and rows sum the same
        for i in range(n):
            assert sum(xs[i][j] for j in range(n)) == c

        for j in range(n):
            assert sum(xs[i][j] for i in range(n)) == c

        # All diagonals sum the same
        assert sum(xs[i][i] for i in range(n)) == c
        assert sum(xs[i][n - 1 - i] for i in range(n)) == c

        # Get the first solution with turbo
        # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
        # only one solution is possible, because the internal structure of the problem is destroyed
        if satisfy(turbo=True):
            print(c)
            for i in range(n):
                print(xs[i])
            print()
            n += 1
        else:
            print('Infeasible ...')
            break
