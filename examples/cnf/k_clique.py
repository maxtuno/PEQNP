import sys

import peqnp.cnf as cnf


def load_file(file_name):
    graph_ = []
    with open(file_name, 'r') as file:
        for line in file.readlines():
            if line.startswith('p edge '):
                n_ = int(line[len('p edge '):].split(' ')[0])
            elif line.startswith('e '):
                x, y = map(int, line[len('e '):].split(' '))
                graph_.append((x, y))
    matrix_ = [[0 for _ in range(n_)] for _ in range(n_)]
    for i, j in graph_:
        matrix_[i - 1][j - 1] = 1
        matrix_[j - 1][i - 1] = 1
    return n_, matrix_


if __name__ == '__main__':

    # python3 k_clique.py frb30-15-5.clq 30 > k_clique.sol
    # ./k_clique_validator frb30-15-1.clq k_clique.sol

    n, adj = load_file(sys.argv[1])
    k = int(sys.argv[2])

    cnf.begin(k.bit_length(), 'k_clique')
    bits = cnf.tensor(dimensions=(n,))
    assert sum(bits[[i]](0, 1) for i in range(n)) == k
    for i in range(n - 1):
        for j in range(i + 1, n):
            if adj[i][j] == 0:
                assert bits[[i]](0, 1) & bits[[j]](0, 1) == 0
    cnf.end({'bits': bits})

    if cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
        print(k)
        print(' '.join([str(i + 1) for i in range(n) if bits.binary[i]]))
    else:
        print('Infeasible ...')

