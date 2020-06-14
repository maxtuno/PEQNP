import matplotlib.pyplot as plt
import numpy as np

import peqnp.sdk as sdk


def plot(I, J=None, X=None, title='Original', obj=0):
    plt.figure(figsize=(10, 10))
    plt.title('{} : {}'.format(title, obj))
    a, b = zip(*I)
    plt.scatter(a, b, c='blue', s=50, alpha=0.6)
    if J is not None:
        if X is not None:
            for i in range(m):
                for j in range(n):
                    if X[i][j]:
                        plt.plot([I[i][0], J[j][0]], [I[i][1], J[j][1]], 'g-', alpha=0.2)
        a, b = zip(*J)
        plt.scatter(a, b, c='red', s=300, alpha=0.8)
    else:
        a, b = zip(*J)
        plt.scatter(a, b, c='red', s=300, alpha=0.8)
    plt.show()
    plt.close()


def oracle(seq):
    global O, glb, n
    M = np.zeros(shape=(m, n))
    for i in range(m):
        for j in range(n):
            M[i][j] = np.linalg.norm(I[i] - J[seq[j]])
    sdk.engine(sat_solver_path='lib/libSLIME.dylib', mip_solver_path='lib/libLP_SOLVE.dylib')
    X = np.asarray(sdk.matrix(dimensions=(m, n), is_mip=True))
    sdk.all_binaries(X.flatten())
    assert sum(X.flatten()) == m
    assert (X.sum(axis=1) == 1).all()
    obj = sdk.minimize(sum(X[i][j] * M[i][j] for i in range(m) for j in range(n)))
    O = np.vectorize(int)(X)
    return obj


if __name__ == '__main__':
    m = 50
    k = 15
    n = 3
    I = np.random.sample(size=(m, 2))
    J = np.random.sample(size=(k, 2))
    plot(I, J)
    seq = sdk.hess_sequence(k, oracle=oracle, fast=False)
    plot(I, J[seq][:n], O, 'www.peqnp.com', oracle(seq))
