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

if __name__ == '__main__':

    engine(10)

    y = integer()
    x = integer()

    assert x + -y == 10

    while satisfy():
        print(x + -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x + -y == 10

    while satisfy(normalize=True):
        print(x + -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x * -y == 10

    while satisfy():
        print(x * -y)

    ################################################################################
    print(80 * '-')

    engine(10)

    y = integer()
    x = integer()

    assert x * -y == 10

    while satisfy(normalize=True):
        print(x * -y)