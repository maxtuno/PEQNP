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
import peqnp as pn

n = 6
m = 3

pn.engine(n.bit_length() + 1)

Y = pn.vector(size=n ** m)

pn.apply_single(Y, lambda k: k < n)

Y = np.reshape(Y, newshape=(m * [n]))

for i in range(n):
    pn.all_different(Y[i])
    pn.all_different(Y.T[i])
    for j in range(n):
        pn.all_different(Y[i][j])
        pn.all_different(Y.T[i][j])

for idx in pn.hyper_loop(m - 1, n):
    s = Y
    for i in idx:
        s = s[i]
        pn.all_different(s)
        pn.all_different(s.T)

if pn.satisfy(turbo=True, log=True):
    y = np.vectorize(int)(Y).reshape(m * [n])
    print(y)
    print(80 * '-')
else:
    print('Infeasible ...')
