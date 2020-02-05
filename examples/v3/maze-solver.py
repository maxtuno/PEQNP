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
import numpy as np
from peqnp import *


# https://gist.github.com/fcogama/3689650

def maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = np.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make isles
    for i in range(density):
        x, y = np.random.randint(0, shape[1] // 2) * 2, np.random.randint(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[np.random.randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    # close the direct path
    Z[1][-2] = True
    Z[2][-2] = True
    return Z


if __name__ == '__main__':

    """
    A simple optimal maze solver is not perfect, need more work...
    """

    m = int(sys.argv[1])
    n = 2 * m

    M = maze(n, m)

    n, m = M.shape

    a, b = 0, 0
    c, d = n - 1, m - 1

    M[a][b] = False
    M[c][d] = False

    for i in range(n):
        for j in range(m):
            if i == a and j == b:
                print('A', end=' ')
                continue
            if i == c and j == d:
                print('B', end=' ')
                continue
            if M[i][j]:
                print('.', end=' ')
            else:
                print(' ', end=' ')
        print()

    print('\n\n')

    opt = n * m
    while True:

        engine(2 * (n + m).bit_length())

        T = tensor(dimensions=(n, m))

        assert T[[a, b]](0, 1) == 1
        assert T[[c, d]](0, 1) == 1
        assert T[[a + 1, b + 1]](0, 1) == 1
        assert T[[c - 1, d - 1]](0, 1) == 1

        for i in range(n):
            for j in range(m):
                if M[i][j]:
                    assert T[[i, j]](0, 1) == 0

        for i in range(1, n):
            for j in range(1, m):
                if not M[i][j]:
                    assert T[[i, j]](1,
                                     T[[i - 1, j]](0, 1) |
                                     T[[i, j - 1]](0, 1) |
                                     T[[i - 1, j - 1]](0, 1)) == 1

        for i in range(n - 1):
            for j in range(m - 1):
                if not M[i][j]:
                    assert T[[i, j]](1,
                                     T[[i + 1, j]](0, 1) |
                                     T[[i, j + 1]](0, 1) |
                                     T[[i + 1, j + 1]](0, 1)) == 1

        assert sum(T[[i, j]](0, 1) for i in range(n) for j in range(m)) < opt

        if satisfy(turbo=True):
            opt = sum(flatten(T.binary))
            for i in range(n):
                for j in range(m):
                    if i == a and j == b:
                        print('A', end=' ')
                        continue
                    if i == c and j == d:
                        print('B', end=' ')
                        continue
                    if M[i][j]:
                        print('.', end=' ')
                        continue
                    if T.binary[i][j]:
                        print('O', end=' ')
                    else:
                        print(' ', end=' ')
                print()
            print()
        else:
            break
