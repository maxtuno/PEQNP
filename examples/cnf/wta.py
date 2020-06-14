import sys

import numpy as np
import peqnp.cnf as cnf

# Ref
# http://i4c.iust.ac.ir/UPL/Paper18/i4c18-1008.pdf
# http://web.karabuk.edu.tr/emrullahsonuc/wta/A_Parallel_Simulated_Annealing_Algorithm_for_Weapon-Target_Assignment_Problem.pdf

# Instances
# http://web.karabuk.edu.tr/emrullahsonuc/wta/

def objective(e):
    return sum(v[i] * np.prod([(1 - pij[i][j]) ** e[i][j] for j in range(n)]) for i in range(n))


def load_instance(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        n = int(lines[0])
        del lines[0]
        v = list(map(int, lines[0:n]))
        del lines[0:n]
        pij = list(map(float, lines))
    return n, v, np.reshape(pij, newshape=(n, n))


if __name__ == '__main__':
    n, v, pij = load_instance(sys.argv[1])
    alpha = 10 ** 4
    bits = int(alpha * sum(v) * pij.sum()).bit_length()
    opt = alpha * sum(v)
    while True:
        cnf.begin(bits, key='wpa')
        X = cnf.tensor(dimensions=(n, n))
        for i in range(n):
            assert sum(X[[i, j]](0, 1) for j in range(n)) == 1
        for j in range(n):
            assert sum(X[[i, j]](0, 1) for i in range(n)) == 1
        assert sum(v[i] * X[[i, j]](1, alpha - pij[i][j] * alpha) for i in range(n) for j in range(n)) < opt
        cnf.end({'X': X})
        if cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
            opt = sum(v[i] * (alpha - pij[i][j] * alpha) if X.binary[i][j] else 1 for i in range(n) for j in range(n))
            print(opt / alpha, objective(np.vectorize(int)(X.binary)))
            for i in range(n):
                for j in range(n):
                    sys.stdout.write(str(int(X.binary[i][j])))
                sys.stdout.write('\n')
        else:
            break
