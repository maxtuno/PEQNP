# PEQNP [1.0.2]

The PEQNP System its a automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3 and 0 dependencies (requirements.txt is only for documentation on readthedocs).

# SLIME 4

Simple: The Best SAT Solver on The Planet.

[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)

To install the latest version:

    pip install PEQNP --upgrade
    
Latin Hyper Cubes:

    import numpy as np
    import peqnp as pn

    n = 6
    m = 3

    pn.engine(n.bit_length() + 1)

    Y = pn.vector(size=n ** m)

    pn.apply_single(Y, lambda k: k < n)

    Y = np.reshape(Y, newshape=(m * [n]))

    for i in range(n):
        pn.all_different(Y[i])
        pn.all_different(Y.T[i])
        for j in range(n):
            pn.all_different(Y[i][j])
            pn.all_different(Y.T[i][j])

    for idx in pn.hyper_loop(m - 1, n):
        s = Y
        for i in idx:
            s = s[i]
            pn.all_different(s)
            pn.all_different(s.T)

    if pn.satisfy(turbo=True, log=True):
        y = np.vectorize(int)(Y).reshape(m * [n])
        print(y)
        print(80 * '-')
    else:
        print('Infeasible ...')

Output:

     [[[4 1 5 2 3 0]
       [1 5 2 4 0 3]
       [5 2 3 0 4 1]
       [2 4 0 3 1 5]
       [0 3 4 1 5 2]
       [3 0 1 5 2 4]]
     
      [[5 0 4 3 1 2]
       [0 4 3 5 2 1]
       [4 3 2 1 5 0]
       [3 5 1 2 0 4]
       [2 1 0 4 3 5]
       [1 2 5 0 4 3]]
     
      [[0 4 3 5 2 1]
       [5 0 4 3 1 2]
       [3 5 1 2 0 4]
       [4 3 2 1 5 0]
       [1 2 5 0 4 3]
       [2 1 0 4 3 5]]
     
      [[1 5 2 4 0 3]
       [4 1 5 2 3 0]
       [2 4 0 3 1 5]
       [5 2 3 0 4 1]
       [3 0 1 5 2 4]
       [0 3 4 1 5 2]]
     
      [[3 2 1 0 4 5]
       [2 3 0 1 5 4]
       [0 1 5 4 3 2]
       [1 0 4 5 2 3]
       [4 5 3 2 1 0]
       [5 4 2 3 0 1]]
     
      [[2 3 0 1 5 4]
       [3 2 1 0 4 5]
       [1 0 4 5 2 3]
       [0 1 5 4 3 2]
       [5 4 2 3 0 1]
       [4 5 3 2 1 0]]]

More info:

PEQNP Home
www.peqnp.science

Twitter Account
https://twitter.com/maxtuno

Youtube Channel
https://www.youtube.com/channel/UCFlk1dUYLKtymcoMScdynNA

Facebook Page
https://www.facebook.com/PEQNP-104747814228901

Documentation
https://peqnp.readthedocs.io

PEQNP Examples
https://github.com/maxtuno/PEQNP/tree/master/examples

Advanced PEQNP Examples
https://github.com/maxtuno/PEQNP_EXAMPLES

