import numpy as np
import peqnp.sdk as sdk
import matplotlib.pyplot as plt


def plot(tour, title):
    x, y = zip(*[data[tour[i]] for i in range(n)] + [data[tour[0]]])
    plt.title(title + ' : {}'.format(oracle(tour)))
    plt.plot(x, y, 'r-')
    plt.plot(x, y, 'ko')
    plt.show()
    plt.close()


def oracle(seq):
    return sum(D[seq[i - 1]][seq[i]] for i in range(n))

n = 10
data = np.random.logistic(size=(n, 2)) * 10
D = np.zeros(shape=(n, n))
for i in range(n):
    for j in range(n):
        D[i][j] = int(np.linalg.norm(data[i] - data[j]))

seq = sdk.hess_sequence(n, oracle=oracle, fast=False)
print(oracle(seq))
plot(seq, 'HESS')

sdk.engine(sat_solver_path='lib/libSLIME.dylib', mip_solver_path='lib/libLP_SOLVE.dylib', info=True)

M = np.asarray(sdk.matrix(dimensions=(n, n), is_mip=True))
u = sdk.vector(size=n, is_mip=True)

for k in range(n):
    assert M[k][k] == 0

assert sum(M.flatten()) == n

for i in range(n):
    for j in range(n):
        assert M[i][j] <= 1

for a, b in zip(M, M.T):
    assert sum(a) == 1
    assert sum(b) == 1

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            assert u[i] - u[j] + (n - 1) * M[i][j] <= n - 2

optimal = sdk.minimize(sum(D[i][j] * M[i][j] for i in range(n) for j in range(n)))
print(optimal)

path = {}
for i in range(n):
    for j in range(n):
        if M[i][j].value:
            path[j] = i

tour = [0, path[0]]
while len(tour) < n:
    tour.append(path[tour[-1]])
plot(tour, 'MIP')

print('ratio HESS / MIP = {}'.format(oracle(seq) / optimal))