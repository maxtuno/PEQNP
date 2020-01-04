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

import numpy as np
from peqnp import *

if __name__ == '__main__':

    # Solving Matrix Equations

    n = 10

    # Define 3 Random Matrices
    A = np.random.randint(0, 10, size=(n, n))
    B = np.random.randint(0, 10, size=(n, n))
    C = np.random.randint(0, 10, size=(n, n))

    # Ensure the entire problem can be represented on the engine
    engine(bits=int(sum((A + B + C).flatten())).bit_length())

    # Show the matrices
    print(A)
    print(B)
    print(C)

    # Declare two integer matrices and convert to numpy arrays
    X = np.asarray(matrix(dimensions=(n, n)))
    Y = np.asarray(matrix(dimensions=(n, n)))

    # The Equation
    assert (np.matmul(A.T, Y ** 2) + np.matmul(A, B) == X.T + np.matmul(Y, C)).all()

    # Get all solutions
    while satisfy():
        print(80 * '-')
        print((np.matmul(A.T, Y ** 2) + np.matmul(A, B) == X.T + np.matmul(Y, C)).all())
        print(80 * '-')
        print(X)
        print(Y)
