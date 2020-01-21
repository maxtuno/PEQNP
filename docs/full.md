# Full System

The PEQNP System include the HESS algorithm, that is a Universal Black Box Optimizer, the Diophantine and MIP Solvers.

# The \(m,n)\-optimal priority problem.

Input: Given a \(P\), \(Q\), \(M)\ and \(m\), a lis of priorities (or probabilities), a list of profits (positives and negatives) and an matrix of costs of size \(n\), \(n\), \(n, n\) and an positive integer n.
Output: Select the sequence of \(m\) elements that make the probability maximal, the profit maximal, and the distance minimal.

```python
import numpy as np
import matplotlib.pyplot as plt
from peqnp import *


def oracle(seq):
    return sum(np.linalg.norm(lc[seq[i]] - lc[seq[i - 1]]) for i in range(len(seq)))


if __name__ == '__main__':

    n = 50
    m = 10

    priorities = np.random.randint(1, 100, size=n)
    profits = np.random.logistic(size=(n, n))
    locations = np.random.logistic(size=(n, 2))

    print('PRIORITIES     : {}'.format(priorities.tolist()))
    print('PROFITS        : {}'.format(profits.tolist()))
    print('LOCATIONS      : {}'.format(locations.tolist()))

    distances = np.zeros(shape=(n, n))
    for i in range(n):
        for j in range(n):
            distances[i][j] = np.linalg.norm(locations[i] - locations[j])

    priority = 0
    while True:

        engine(10)
        
        # declare the integer to store the selected elements for maximal priority.
        select = integer(bits=n)
    
        # maximality condition
        assert sum(switch(select, i, neg=True) * priorities[i] for i in range(n)) > priority
        
        # only m elements
        assert sum(switch(select, i, neg=True) for i in range(n)) == m
    
        # solve
        if satisfy(turbo=True):

            priority = sum(priorities[i] for i in range(n) if select.binary[i])

            print('\nSELECTED   : {}'.format([i for i in range(select.bits) if select.binary[i]]))
            print('PRIORITIES : {}'.format(priority))
        
            # a matrix of linear (n, n)-variables
            x = np.asarray(matrix(is_mip=True, dimensions=(n, n)))

            # all linear variables are binaries
            apply_single(flatten(x), lambda k: k <= 1)
        
            # diagonal of matrix is zero, and only one element by row and column.
            for i, (row, col) in enumerate(zip(x, x.T)):
                assert x[i][i] == 0
                assert sum(row) == 1
                assert sum(col) == 1
    
            # filter the profits with selected priorities
            selected_profits = mul(profits, select.binary)
        
            # macimize profit with selected elements
            print('PROFIT     : {}'.format(maximize(dot(flatten(selected_profits), flatten(x)))))
            
            # get the locations for the selected elements
            lc = []
            for i in range(n):
                if select.binary[i]:
                    lc.append(locations[i])
        
            # minimize dstance for selected elements and get the secuence.
            seq = hess_sequence(m, oracle)
    
            # show solution
            opt = oracle(seq)
            print('DISTANCE   : {}\nSEQ        : {}'.format(opt, seq))
            plt.figure(figsize=(10, 10))
            plt.title('priorities Problem with PEQNP - www.peqnp.science')
            u, v = zip(*locations)
            plt.scatter(u, v, s=5 * priorities[seq], c='b', alpha=0.7)
            u, v = zip(*[lc[i] for i in seq + [seq[0]]])
            plt.plot(u, v, 'k-')
            plt.scatter(u, v, s=20 * priorities[seq], c='r')
            plt.savefig('optimal-priority-problem.png')
            plt.close()
        else:
            break
```
