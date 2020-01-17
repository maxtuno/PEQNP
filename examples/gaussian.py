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


def test1():
    engine(5)

    x = integer()
    y = integer()
    z = gaussian(x, y)

    apply_single([x, y], lambda k: k < oo())

    assert z * z.conjugate() == abs(z)

    while satisfy():
        print(z, complex(z) + complex(z).conjugate() == abs(z))


def test2():
    engine(10)

    x = integer()
    y = integer()

    z = gaussian(x, y)

    apply_single([x, y], lambda k: k < oo())

    assert 1 < abs(z).real < 10

    while satisfy():
        print(z, 1 < abs(complex(z)) < 10)


def test3():
    engine(bits=4)

    x = integer()
    y = integer()

    z = integer()
    w = integer()

    s = integer()
    t = integer()

    a = gaussian(x, y)
    b = gaussian(z, w)
    c = gaussian(s, t)

    apply_single([z, y, z, w, s, t], lambda k: k < 2 ** (bits() - 1) - 1)

    assert a ** 3 + b ** 2 + a * b == a + b + c

    assert a != 0
    assert b != 0
    assert c != 0

    while satisfy():
        print(a, b, c, complex(a) ** 3 + complex(b) ** 2 + complex(a) * complex(b) == complex(a) + complex(b) + complex(c))


def test4():
    rsa = complex(31 * 97, 43 * 101)

    engine(int(max(rsa.real, rsa.imag)).bit_length())

    x = integer()
    y = integer()
    z = integer()
    w = integer()

    p = gaussian(x, y)
    q = gaussian(z, w)

    apply_single([x, y, z, w], lambda k: 0 < k < 128)

    assert p * q == rsa

    while satisfy():
        print(p, q, complex(p) * complex(q) == rsa)


if __name__ == '__main__':
    print(80 * '-')
    test1()
    print(80 * '-')
    test2()
    print(80 * '-')
    test3()
    print(80 * '-')
    test4()
