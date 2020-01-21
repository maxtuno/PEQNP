"""
Copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

from peqnp import *

if __name__ == '__main__':

    print('This generate the first 10 magic squares')

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
