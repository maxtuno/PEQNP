# PEQNP 

The PEQNP System its an automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3 and 2 with 0 dependencies.

# SLIME 4

[The Best SAT Solver on The Planet](https://github.com/maxtuno/SLIME)

[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)

    [PEQNP + SLIME 4 : 1.2.2 - 12-5-2020]

To install the latest version:

    pip install PEQNP --upgrade

[Home](https://www.peqnp.com) [Twitter](https://twitter.com/maxtuno) [Youtube](https://www.youtube.com/channel/UCFlk1dUYLKtymcoMScdynNA) [Facebook](https://www.facebook.com/PEQNP-104747814228901) [Documentation](https://peqnp.readthedocs.io) [Examples](https://github.com/maxtuno/PEQNP/tree/master/examples) [Advanced](https://github.com/maxtuno/PEQNP_EXAMPLES)

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

PIXIE: Otional submodule for Mixed Integer Programming. 

    [PEQNP + SLIME 4 + PIXIE : 1.2.2 - 12-5-2020]

To install submodule:

    pip install PEQNP --force --install-option=pixie

Simple MIP:

    import peqnp as pn

    pn.engine()

    x0 = pn.linear(is_real=True)
    x1 = pn.linear()
    x2 = pn.linear()
    x3 = pn.linear()
    assert +0.5420 * x0 - 0.4835 * x1 + 1.5304 * x2 + 0.0000 * x3 <= -2.0000
    assert +1.7801 * x0 + 0.0000 * x1 + 1.4747 * x2 + 0.0000 * x3 <= 3.0000
    assert x0 <= 6.0000
    assert x1 <= 6.0000
    assert x2 <= 1.0000
    assert x3 <= 7.0000
    print(pn.minimize(-13.3221 * x0 + 1.0028 * x1 + 2.3615 * x2 - 53.7288 * x3))
    print(x0)
    print(x1)
    print(x2)
    print(x3)

  Output:

    -392.2309477859779
    1.6623616236162357
    6
    0
    7
