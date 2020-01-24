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

import time
import sys

import numpy as np
import matplotlib.pyplot as plt

from peqnp import *

if __name__ == '__main__':

    # the bits bits for the elements on the matrix
    bits = 32

    for boost in [True, False]:

        ini = time.time()
        times = []
        sizes = []

        np.random.seed(0)

        # the dimensions of the matrix
        for n in range(1, 10):
            for m in range(1, 10):

                # The matrix
                cc = np.random.randint(0, 2 ** bits, size=(n, m))
                # Ensure that solution exist (for gen some interesting example)
                d = np.dot(cc, np.random.randint(0, 2, size=(m,)))

                print(cc)
                print(d)

                # Setup the engine with the bits of the sum of all values of the matrix, this ensure that the entire problem is well represented represented on the system.
                engine(bits=int(np.sum(cc)).bit_length())

                # Declare a m-sized vector
                xs = vector(size=m)

                # All element of the vector are binaries, i.e. 0 or 1
                all_binaries(xs)

                # The main constrain for the problem (there is a one of the Karp's 21 NP-complete problems https://people.eecs.berkeley.edu/~luca/cs172/karp.pdf)
                assert (np.dot(cc, xs) == d).all()

                # Get the first solution with turbo
                # very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
                # only one solution is possible, because the internal structure of the problem is destroyed
                if satisfy(turbo=True, boost=boost):
                    print(xs)
                    print(np.dot(cc, xs))
                    print()
                else:
                    print('Infeasible...')
                    raise Exception('ERROR! - Increase the bits for engine...')

                times.append(time.time() - ini)
                sizes.append(n * m)

        plt.plot(sizes, times, 'k-')
        plt.plot(sizes, times, 'r.')
        plt.title('{}'.format('BOOST' if boost else 'no-BOOST'))
        plt.savefig('01-integer-programming_{}.png'.format('boost' if boost else 'no-boost'))
        plt.close()