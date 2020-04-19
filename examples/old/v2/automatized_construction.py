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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from peqnp import *

if __name__ == '__main__':

    """
    Given a set of pieces and a plane of construction, get the optimal sequence on distance for construct the plane.
    """

    n = 20

    O = np.random.randint(0, 4, size=n)
    I = O.copy()
    np.random.shuffle(I)

    L = np.asarray([(i, (n - i)) for i in range(n)])
    M = np.random.logistic(size=(n, 2))

    Q = np.zeros(shape=(n, n))
    for i in range(n):
        for j in range(n):
            Q[i][j] = np.linalg.norm(L[i] - M[j])

    print(80 * '=')
    print(I)
    print(O)

    opt = 1000
    while True:

        engine(10)

        a, b = matrix_permutation(Q.flatten(), n)
        x, y = permutations(I, n)

        for i in range(n):
            assert y[i] == O[i]
            assert x[i] == a[i]

        assert sum(b) < opt

        if satisfy(turbo=True):
            x = np.vectorize(int)(x)

            fig = plt.figure(figsize=(10, 10))
            plt.title('Automatized Construction with PEQNP')
            ax = fig.add_subplot(111)

            u, v = zip(*L)
            plt.scatter(u, v, c='g', s=O * 200, alpha=0.5)
            u, v = zip(*M[x])
            plt.scatter(u, v, c='b', s=I[x] * 200, alpha=0.5)

            opt = sum(b)
            print(opt)
            for i in range(n):
                if i % n == 0:
                    print(' ')
                print(x[i], end=' ')
                ax.annotate(['A', 'T', 'G', 'C'][O[x][i]], (L[x][i][0], L[x][i][1]), size=20, color='k')
                ax.annotate(x[i], (M[x][i][0], M[x][i][1]), size=20, color='k')
                ax.add_line(Line2D([L[i][0], M[x][i][0]], [L[i][1], M[x][i][1]], c='r'))
            plt.savefig('automatized_construction.png')
            plt.close()
        else:
            break
