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

    bits = 6

    print(80 * '-')
    print(' ** ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x ** y == z
    while satisfy():
        print(x, y, z)
        if x.value ** y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print('pow_mod')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    w = integer()
    assert pow(x, y, z) == w
    while satisfy():
        print(x, y, z)
        if pow(x.value, y.value, z.value) != w.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' * ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x * y == z
    while satisfy():
        print(x, y, z)
        if x.value * y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' / ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x / y == z
    while satisfy():
        print(x, y, z)
        if x.value / y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' + ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x + y == z
    while satisfy():
        print(x, y, z)
        if x.value + y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' - ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x - y == z
    while satisfy():
        print(x, y, z)
        if x.value - y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' % ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x % y == z
    while satisfy():
        print(x, y, z)
        if x.value % y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' & ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x & y == z
    while satisfy():
        print(x, y, z)
        if x.value & y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' | ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x | y == z
    while satisfy():
        print(x, y, z)
        if x.value | y.value != z.value:
            raise Exception('BUG!')

    print(80 * '-')
    print(' ^ ')
    print(80 * '-')

    engine(bits)
    x = integer()
    y = integer()
    z = integer()
    assert x ^ y == z
    while satisfy():
        print(x, y, z)
        if x.value ^ y.value != z.value:
            raise Exception('BUG!')
