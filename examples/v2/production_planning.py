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

"""
Production Planning

A firm is attempting to optimise its production plan by bearing in mind the fol-
lowing profit function:
f = ln(1 + x1 + x2)
Besides, the following capacity constraint is also considered:
By taking into account that 1 machining hour is required to produce x1 and 2
machining hours are needed to produce x2 , it is necessary to consider that only a
total of 5 machining hours per day is available.

From Operations Research Problems - Statements and Solutions p-104 
"""


def f(x1, x2):
    return np.log(1 + x1 + x2)


def constraints(x1, x2):
    return x1 + 2 * x2 <= 5


def oracle(seq):
    global glb
    x1, x2 = xx1[seq[0]], xx2[seq[1]]
    if constraints(x1, x2):
        loc = f(x1, x2)
        if loc > glb:
            glb = loc
            print(glb, x1, x2)
        return -loc
    return np.inf


if __name__ == '__main__':
    glb, top = 0, 0

    n = 100

    for _ in range(n):

        xx1 = np.linspace(0, 5, n)
        xx2 = np.linspace(0, 5, n)

        np.random.shuffle(xx1)
        np.random.shuffle(xx2)

        seq = hess_sequence(n, oracle)

        x1 = xx1[seq[0]]
        x2 = xx2[seq[1]]

        if glb > top:
            top = glb
            print(x1, x2, constraints(x1, x2), f(x1, x2))
