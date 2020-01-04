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

from peqnp import *

if __name__ == '__main__':

    # Gaussian Integers Equation

    # Initialize the engine
    engine(bits=10)

    # Declare real and imaginary integers
    p1 = integer()
    q1 = integer()

    p2 = integer()
    q2 = integer()

    p3 = integer()
    q3 = integer()

    # Declare thr gaussian integers from real and imaginary integers
    x = gaussian(p1, q1)
    y = gaussian(p2, q2)
    z = gaussian(p3, q3)

    # Declare the exponent
    a = integer()
    b = integer()
    c = integer()

    # The main constraint
    assert gaussian(a, 0) * x ** 3 + gaussian(b, 0) * y ** 2 == gaussian(c, 0) * z ** c

    assert p1 * q1 > a
    assert p2 * p2 > b
    assert p3 * p3 > c

    # only interesting solutions
    assert a > 1
    assert b > 1
    assert c > 1

    # Get all solutions
    while satisfy():
        print('{3} * {0} ** 3 + {4} * {1} ** 2 == {5} * {2} ** {5}'.format(x, y, z, a, b, c))
