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

    engine(16)

    c = integer()

    X = np.reshape(vector(size=(n ** k)), newshape=k * [n])

    apply_single(X.flatten(), lambda x: x > 0)

    for x in X:
        for i in range(n):
            assert sum(x[i]) == c
            assert sum(x.T[i]) == c
        assert sum([x[i][i] for i in range(n)]) == c
        assert sum([x[n - 1 - i][i] for i in range(n)]) == c

    for x in X.T:
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
    c Reduced to 32028 vars, 212208 cls (grow=0)
    c 28.82 % 	 
    --------------------------------------------------------------------------------
    [[[5985 3655 2706 36831 14357]
      [3477 17466 30319 10070 2202]
      [25358 6392 21980 2 9802]
      [22535 10948 5337 2822 21892]
      [6179 25073 3192 13809 15281]]
    
     [[2667 20095 16296 987 23489]
      [17058 25309 12693 6237 2237]
      [6836 6894 3121 36371 10312]
      [16431 10145 29119 6390 1449]
      [20542 1091 2305 13549 26047]]
    
     [[13067 20270 19750 7762 2685]
      [8219 864 8704 8232 37515]
      [21769 297 13845 9720 17903]
      [921 19214 5226 34250 3923]
      [19558 22889 16009 3570 1508]]
    
     [[30009 7707 18891 814 6113]
      [7349 16212 11487 16475 12011]
      [2499 13517 6896 16271 24351]
      [12572 22945 9261 4057 14699]
      [11105 3153 16999 25917 6360]]
    
     [[11806 11807 5891 17140 16890]
      [27431 3683 331 22520 9569]
      [7072 36434 17692 1170 1166]
      [11075 282 14591 16015 21571]
      [6150 11328 25029 6689 14338]]]
    --------------------------------------------------------------------------------
    TIME : 715.5 (s)
    """
