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
ref: http://www.trump.de/magic-squares/magic-cubes/cubes-1.html#order4
"""

if __name__ == '__main__':

    start = time.time()

    n = 4
    k = 3

    engine(10)

    c = integer()

    X = np.reshape(vector(size=(n ** k)), newshape=k * [n])

    apply_single(X.flatten(), lambda x: x > 0)

    for x in X:
        for i in range(n):
            assert sum(x[i]) == c
            assert sum(x.T[i]) == c
        assert sum([x[i][i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][i] for i in range(n)]) == c

    assert sum([X[i][i][i] for i in range(n)]) == c
    assert sum([X[n - 1 - i][i][i] for i in range(n)]) == c
    assert sum([X[i][n - 1 - i][i] for i in range(n)]) == c
    assert sum([X[i][i][n - 1 - i] for i in range(n)]) == c

    for i in range(n):
        assert sum([X[i][j][j] for j in range(n)]) == c
        assert sum([X[j][i][j] for j in range(n)]) == c
        assert sum([X[j][j][i] for j in range(n)]) == c

        assert sum([X[j][i][i] for j in range(n)]) == c
        assert sum([X[i][j][i] for j in range(n)]) == c
        assert sum([X[i][i][j] for j in range(n)]) == c

        assert sum([X.T[i][j][j] for j in range(n)]) == c
        assert sum([X.T[j][i][j] for j in range(n)]) == c
        assert sum([X.T[j][j][i] for j in range(n)]) == c

        assert sum([X.T[j][i][i] for j in range(n)]) == c
        assert sum([X.T[i][j][i] for j in range(n)]) == c
        assert sum([X.T[i][i][j] for j in range(n)]) == c

        assert sum([X[i].T[j][j] for j in range(n)]) == c
        assert sum([X[j].T[i][j] for j in range(n)]) == c
        assert sum([X[j].T[j][i] for j in range(n)]) == c

        assert sum([X[j].T[i][i] for j in range(n)]) == c
        assert sum([X[i].T[j][i] for j in range(n)]) == c
        assert sum([X[i].T[i][j] for j in range(n)]) == c

        assert sum([X[i][j].T[j] for j in range(n)]) == c
        assert sum([X[j][i].T[j] for j in range(n)]) == c
        assert sum([X[j][j].T[i] for j in range(n)]) == c

        assert sum([X[j][i].T[i] for j in range(n)]) == c
        assert sum([X[i][j].T[i] for j in range(n)]) == c
        assert sum([X[i][i].T[j] for j in range(n)]) == c

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
    c Reduced to 8490 vars, 55376 cls (grow=0)
    c 33.29 % 	 
    --------------------------------------------------------------------------------
    [[[378 113 231 222]
      [316 254 173 201]
      [6 305 212 421]
      [244 272 328 100]]
    
     [[98 239 527 80]
      [177 179 172 416]
      [347 370 223 4]
      [322 156 22 444]]
    
     [[96 335 99 414]
      [581 249 102 12]
      [139 300 293 212]
      [128 60 450 306]]
    
     [[372 75 269 228]
      [124 262 211 347]
      [198 255 216 275]
      [250 352 248 94]]]
    --------------------------------------------------------------------------------
    TIME : 52.89 (s)
    """
