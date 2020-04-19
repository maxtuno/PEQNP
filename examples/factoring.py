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

import sys

import peqnp as pn

if __name__ == '__main__':

    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Usage   : python3 factoring.py rsa-number')
        print('Example : python3 factoring.py 3007')
        exit(0)

    # The number to factoring.
    rsa = int(sys.argv[1])

    # Ensure that the problem can be fully represented.
    pn.engine(bits=rsa.bit_length())

    # The two factors.
    p, q = pn.integer(), pn.integer()

    # The main constraint
    assert p * q == rsa

    # Discard the trivial cases and symmetries.
    assert 1 < p < q < rsa

    # Get the first solution with turbo
    # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
    # only one solution is possible, because the internal structure of the problem is destroyed
    if pn.satisfy(turbo=True):
        print(p, q)
    else:
        print('Is Prime!')
