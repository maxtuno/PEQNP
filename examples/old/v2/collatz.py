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

from peqnp import *


def collatz(n):
    ss = []
    while n > 1:
        if n % 2:
            n = 3 * n + 1
            ss.append(n)

        else:
            n = n // 2
            ss.append(n)
    return ss


def cz0(n):
    assert n % _2 == 0
    return n / _2


def cz1(n):
    assert n % _2 == 1
    return 3 * n + 1


if __name__ == '__main__':

    """
    List all numbers x,y on bit range 10 with the same Collatz sequence.
    """

    engine(10)

    _2 = constant(value=2)

    x = integer()
    y = integer()

    assert cz0(x) == cz1(y)

    assert x > 1
    assert y > 1

    while satisfy():
        print('({}, {})'.format(x, y))
        if collatz(x.value) != collatz(y.value):
            raise Exception('ERROR!')
