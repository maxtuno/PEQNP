"""
Copyright (c) 2012-2020 Oscar Riveros. all rights reserved. contact@peqnp.science

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
import numpy as np
from peqnp import *

"""
ref: http://www.trump.de/magic-squares/magic-cubes/cubes-1.html
"""

if __name__ == '__main__':

    start = time.time()

    n = 5
    k = 3

    engine(6)

    c = integer()

    X = np.reshape(vector(size=(n ** k)), newshape=k * [n])

    apply_single(X.flatten(), lambda x: x > 0)
    # different = ?
    # all_different(X.flatten()[:different])

    for x in X:
        for i in range(n):
            assert sum(x[i]) == c
            assert sum(x[n - 1 - i]) == c
            assert sum(x.T[i]) == c
            assert sum(x.T[n - 1 - i]) == c
        assert sum([x[i][i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][i] for i in range(n)]) == c
        assert sum([x[i][n - 1 - i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][n - 1 - i] for i in range(n)]) == c
        assert sum([x.T[i][i] for i in range(n)]) == c
        assert sum([x.T[n - 1 - i][i] for i in range(n)]) == c
        assert sum([x.T[i][n - 1 - i] for i in range(n)]) == c
        assert sum([x.T[n - 1 - i][n - 1 - i] for i in range(n)]) == c

    for x in X.T:
        for i in range(n):
            assert sum(x[i]) == c
            assert sum(x[n - 1 - i]) == c
            assert sum(x.T[i]) == c
            assert sum(x.T[n - 1 - i]) == c
        assert sum([x[i][i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][i] for i in range(n)]) == c
        assert sum([x[i][n - 1 - i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][n - 1 - i] for i in range(n)]) == c
        assert sum([x.T[i][i] for i in range(n)]) == c
        assert sum([x.T[n - 1 - i][i] for i in range(n)]) == c
        assert sum([x.T[i][n - 1 - i] for i in range(n)]) == c
        assert sum([x.T[n - 1 - i][n - 1 - i] for i in range(n)]) == c

    assert sum([X[i][i][i] for i in range(n)]) == c
    assert sum([X[i][i][n - 1 - i] for i in range(n)]) == c
    assert sum([X[i][n - 1 - i][i] for i in range(n)]) == c
    assert sum([X[i][n - 1 - i][n - 1 - i] for i in range(n)]) == c
    assert sum([X[n - 1 - i][i][i] for i in range(n)]) == c
    assert sum([X[n - 1 - i][i][n - 1 - i] for i in range(n)]) == c
    assert sum([X[n - 1 - i][n - 1 - i][i] for i in range(n)]) == c
    assert sum([X[n - 1 - i][n - 1 - i][n - 1 - i] for i in range(n)]) == c

    assert sum([X.T[i][i][i] for i in range(n)]) == c
    assert sum([X.T[i][i][n - 1 - i] for i in range(n)]) == c
    assert sum([X.T[i][n - 1 - i][i] for i in range(n)]) == c
    assert sum([X.T[i][n - 1 - i][n - 1 - i] for i in range(n)]) == c
    assert sum([X.T[n - 1 - i][i][i] for i in range(n)]) == c
    assert sum([X.T[n - 1 - i][i][n - 1 - i] for i in range(n)]) == c
    assert sum([X.T[n - 1 - i][n - 1 - i][i] for i in range(n)]) == c
    assert sum([X.T[n - 1 - i][n - 1 - i][n - 1 - i] for i in range(n)]) == c

    for j in range(n):
        assert sum([X[j][i][i] for i in range(n)]) == c
        assert sum([X[j][i][n - 1 - i] for i in range(n)]) == c
        assert sum([X[j][n - 1 - i][i] for i in range(n)]) == c
        assert sum([X[j][n - 1 - i][n - 1 - i] for i in range(n)]) == c
        assert sum([X[n - 1 - j][i][i] for i in range(n)]) == c
        assert sum([X[n - 1 - j][i][n - 1 - i] for i in range(n)]) == c
        assert sum([X[n - 1 - j][n - 1 - i][i] for i in range(n)]) == c
        assert sum([X[n - 1 - j][n - 1 - i][n - 1 - i] for i in range(n)]) == c

        assert sum([X.T[j][i][i] for i in range(n)]) == c
        assert sum([X.T[j][i][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[j][n - 1 - i][i] for i in range(n)]) == c
        assert sum([X.T[j][n - 1 - i][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - j][i][i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - j][i][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - j][n - 1 - i][i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - j][n - 1 - i][n - 1 - i] for i in range(n)]) == c

    for j in range(n):
        assert sum([X[i][j][i] for i in range(n)]) == c
        assert sum([X[i][j][n - 1 - i] for i in range(n)]) == c
        assert sum([X[i][n - 1 - j][i] for i in range(n)]) == c
        assert sum([X[i][n - 1 - j][n - 1 - i] for i in range(n)]) == c
        assert sum([X[n - 1 - i][j][i] for i in range(n)]) == c
        assert sum([X[n - 1 - i][j][n - 1 - i] for i in range(n)]) == c
        assert sum([X[n - 1 - i][n - 1 - j][i] for i in range(n)]) == c
        assert sum([X[n - 1 - i][n - 1 - j][n - 1 - i] for i in range(n)]) == c

        assert sum([X.T[i][j][i] for i in range(n)]) == c
        assert sum([X.T[i][j][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[i][n - 1 - j][i] for i in range(n)]) == c
        assert sum([X.T[i][n - 1 - j][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][j][i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][j][n - 1 - i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][n - 1 - j][i] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][n - 1 - j][n - 1 - i] for i in range(n)]) == c

    for j in range(n):
        assert sum([X[i][i][j] for i in range(n)]) == c
        assert sum([X[i][i][n - 1 - j] for i in range(n)]) == c
        assert sum([X[i][n - 1 - i][j] for i in range(n)]) == c
        assert sum([X[i][n - 1 - i][n - 1 - j] for i in range(n)]) == c
        assert sum([X[n - 1 - i][i][j] for i in range(n)]) == c
        assert sum([X[n - 1 - i][i][n - 1 - j] for i in range(n)]) == c
        assert sum([X[n - 1 - i][n - 1 - i][j] for i in range(n)]) == c
        assert sum([X[n - 1 - i][n - 1 - i][n - 1 - j] for i in range(n)]) == c

        assert sum([X.T[i][i][j] for i in range(n)]) == c
        assert sum([X.T[i][i][n - 1 - j] for i in range(n)]) == c
        assert sum([X.T[i][n - 1 - i][j] for i in range(n)]) == c
        assert sum([X.T[i][n - 1 - i][n - 1 - j] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][i][j] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][i][n - 1 - j] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][n - 1 - i][j] for i in range(n)]) == c
        assert sum([X.T[n - 1 - i][n - 1 - i][n - 1 - j] for i in range(n)]) == c

    if satisfy(turbo=True, boost=True, log=True):
        print(80 * '-')
        print(X)
        print(80 * '-')
    else:
        print('Infeasible ...')

    end = time.time()

    print('TIME : {:.4} (s)'.format(end - start))

    """
    c                                          
    c    ██████  ██▓     ██▓ ███▄ ▄███▓▓█████  
    c  ▒██    ▒ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▓█   ▀  
    c  ░ ▓██▄   ▒██░    ▒██▒▓██    ▓██░▒███    
    c    ▒   ██▒▒██░    ░██░▒██    ▒██ ▒▓█  ▄  
    c  ▒██████▒▒░██████▒░██░▒██▒   ░██▒░▒████▒ 
    c  ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░░░ ▒░ ░ 
    c  ░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░░  ░      ░ ░ ░  ░ 
    c  ░  ░  ░    ░ ░    ▒ ░░      ░      ░    
    c        ░      ░  ░ ░         ░      ░  ░ 
    c                                          
    c         http://www.peqnp.science         
    c                                          
    c Reduced to 23804 vars, 154833 cls (grow=0)
    c 32.21 % 	 
    --------------------------------------------------------------------------------
    [[[9 19 6 10 16]
      [14 6 13 16 11]
      [13 9 23 11 4]
      [21 2 6 12 19]
      [3 24 12 11 10]]
    
     [[16 7 31 5 1]
      [6 25 4 16 9]
      [10 2 4 17 27]
      [4 15 17 8 16]
      [24 11 4 14 7]]
    
     [[11 16 8 10 15]
      [11 7 2 16 24]
      [25 4 12 12 7]
      [12 16 14 17 1]
      [1 17 24 5 13]]
    
     [[8 15 11 17 9]
      [12 14 15 11 8]
      [8 23 12 14 3]
      [10 6 20 5 19]
      [22 2 2 13 21]]
    
     [[16 3 4 18 19]
      [17 8 26 1 8]
      [4 22 9 6 19]
      [13 21 3 18 5]
      [10 6 18 17 9]]]
    --------------------------------------------------------------------------------
    TIME : 133.4 (s)
    """
