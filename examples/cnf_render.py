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
    # declare a 2 bits engine
    engine(2)

    # x and y two names integers
    x = integer(key='x')
    y = integer(key='y')

    # simple constraints
    assert x <= 10
    assert y <= 10

    assert x * y == 6

    # This export the problem to CNF format and include the literals mapping for x and y to decode offline
    satisfy(solve=False, cnf_path='test.cnf')

    """
    c PEQNP - www.peqnp.science
    c contact@peqnp.science
    c pip install PEQNP
    p cnf 10 23
    -1 -2 0
    -3 -4 0
    1 -5 0
    -1 5 0
    -2 -6 0
    2 6 0
    -5 6 0
    3 -7 0
    -3 7 0
    -4 -8 0
    4 8 0
    -7 8 0
    -1 -3 0
    -1 -4 9 0
    4 -9 0
    1 -9 0
    -2 -3 10 0
    3 -10 0
    2 -10 0
    -2 -4 0
    9 10 0
    -9 -10 0
    c {'x': [2, 3], 'y': [4, 5]}
    """
