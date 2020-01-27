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
from peqnp import *

if __name__ == '__main__':

    n = 5
    m = 3

    engine((n * (n + 1) // 2).bit_length())

    Y = vector(size=n ** m)

    apply_single(Y, lambda k: 1 <= k <= n)

    Y = np.reshape(Y, newshape=(m * [n]))

    for i in range(n):
        all_different(Y[i])
        all_different(Y.T[i])
        for j in range(n):
            all_different(Y[i][j])
            all_different(Y.T[i][j])

    for idx in hyper_loop(m - 1, n):
        s = Y
        for i in idx:
            s = s[i]
            all_different(s)
            all_different(s.T)

    if satisfy(turbo=True, log=True):
        y = np.vectorize(int)(Y).reshape(m * [n])
        print(y)
        print(80 * '-')
    else:
        print('Infeasible ...')
