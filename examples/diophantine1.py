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

    # On Diophantine equation x^4 + y^4 = n(u^4 + v^4)
    # https://www.degruyter.com/view/j/ms.2019.69.issue-6/ms-2017-0305/ms-2017-0305.xml

    bits = 16

    engine(bits)

    x, y, u, v, n = vector(size=5)

    assert x ** 4 + y ** 4 == n * (u ** 4 + v ** 4)

    assert x > 1
    assert y > 1
    assert u > 1
    assert v > 1
    assert n > 1

    while satisfy():
        print('{0} ** 4 + {1} ** 4 == {4} * ({2} ** 4 + {3} ** 4)'.format(x, y, u, v, n))
