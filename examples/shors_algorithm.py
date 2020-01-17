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
import math
from peqnp import *

if __name__ == '__main__':

    # How Quantum Computers Break Encryption | Shor's Algorithm Explained
    # https://www.youtube.com/watch?v=lvTqbM5Dq4Q

    # Use only small values (Intense RAM Use)
    rsa = 17 * 19

    bits = rsa.bit_length()
    while True:

        print(bits)

        engine(bits, bits // 4)

        g = integer()
        p = integer()
        m = integer()

        assert g ** p == m * rsa + 1
        
        assert g > 2
        assert p > 2
        assert m > 0

        if satisfy(turbo=True):
            g, p, m = int(g), int(p), int(m)
            print('g: {}, p: {}, m: {}'.format(g, p, m))
            x, y = math.gcd(rsa, g ** (p // 2) - 1), math.gcd(rsa, g ** (p // 2) + 1)
            if 1 < x < rsa or 1 < y < rsa:
                if rsa % x == 0 or rsa % y == 0:
                    print('=> {}, {}'.format(x, y))
                    break
        
        bits += 1
