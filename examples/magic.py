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


import peqnp as pn

if __name__ == '__main__':

    n = 3

    # Ensure the problem can be represented
    pn.engine(10)

    # The value that all columns, rows and diagonal sum
    c = pn.integer()

    # A matrix of integers of dimension nxn
    xs = pn.matrix(dimensions=(n, n))

    # All elements are nonzero
    pn.apply_single(pn.flatten(xs), lambda x: x > 0)

    # All elements are different (is magic square)
    pn.apply_dual(pn.flatten(xs), lambda a, b: a != b)

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
    if pn.satisfy(turbo=True, log=True):
        print(c)
        for i in range(n):
            print(xs[i])
        print()
        n += 1
    else:
        print('Infeasible ...')
