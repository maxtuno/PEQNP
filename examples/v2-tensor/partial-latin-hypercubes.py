import numpy as np
from peqnp import *

if __name__ == '__main__':

    n = 6
    m = 3

    engine((n + 1).bit_length())

    X = tensor(dimensions=m * [n])
    Y = vector(size=n ** m)

    apply_single(Y, lambda k: 1 <= k <= n)

    t = np.empty(shape=n ** m, dtype=Entity)
    for k, idx in enumerate(hyper_loop(m, n)):
        t[k] = X[idx](0, Y[k])
    t = t.reshape(m * [n])

    for k in range(n):
        all_different(t[k])
        all_different(t.T[k])
        for l in range(n):
            all_different(t[k][l])
            all_different(t.T[k][l])

    for idx in hyper_loop(m - 1, n):
        s = t
        for k in idx:
            s = s[k]
            all_different(s)
            all_different(s.T)

    if satisfy(turbo=True, boost=True, log=True):
        x = np.vectorize(int)(X.binary)
        y = np.vectorize(int)(Y).reshape(m * [n])
        print(x * y)
        print(80 * '-')
    else:
        print('Infeasible ...')
