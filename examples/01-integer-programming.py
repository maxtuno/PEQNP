"""
copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science
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

    bits = 10
    n, m = 5, 10

    cc = np.random.randint(0, 2 ** bits, size=(n, m))
    d = np.dot(cc, np.random.randint(0, 2, size=(m,)))

    print(cc)
    print(d)

    engine(bits=int(np.sum(cc)).bit_length())

    xs = vector(size=m)

    all_binaries(xs)

    assert (np.dot(cc, xs) == d).all()

    if satisfy(turbo=True):
        print(xs)
        print(np.dot(cc, xs))
    else:
        print('Infeasible...')
