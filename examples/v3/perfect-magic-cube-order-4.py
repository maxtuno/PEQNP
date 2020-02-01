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

    engine(8)

    c = integer()

    X = np.reshape(vector(size=(n ** k)), newshape=k * [n])

    apply_single(X.flatten(), lambda x: x > 0)
    all_different(X.flatten()[n:])

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
    c Reduced to 11270 vars, 63081 cls (grow=0)
    c 48.82 % 	 
    --------------------------------------------------------------------------------
    [[[128 54 37 1]
      [10 33 82 95]
      [16 71 34 99]
      [66 62 67 25]]
    
     [[47 70 15 88]
      [76 73 3 68]
      [32 64 80 44]
      [65 13 122 20]]
    
     [[86 38 22 74]
      [30 110 69 11]
      [51 24 17 128]
      [53 48 112 7]]
    
     [[5 154 40 21]
      [9 57 6 148]
      [14 1 156 49]
      [192 8 18 2]]]
    --------------------------------------------------------------------------------
    TIME : 0.6833 (s)
    """
