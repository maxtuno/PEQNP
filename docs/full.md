# Full System

The PEQNP System include the HESS algorithm, that is a Universal Black Box Optimizer, the Diophantine and MIP Solvers.

# The \(m,n)\-optimal priority problem

Input: Given a \(P\), \(Q\), \(M\) and \(m\), a lis of priorities (or probabilities), a list of profits (positives and negatives) and an matrix of costs.

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

# Partial Latin Hyper Cubes with Tensors

A multi-dimensional latin square with an empty element.

```python
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
```

# Travelling Salesman Problem with HESS

The TSP problem optimized with the Universal Black Box Solver HESS.

```python
import matplotlib.pyplot as plt
import numpy
from peqnp import *

glb = numpy.inf


def oracle(seq):
    global glb
    loc = sum(numpy.linalg.norm(data[seq[i]] - data[seq[(i + 1) % len(seq)]]) for i in range(n))
    if loc < glb:
        glb = loc
        print('Tour Length {}'.format(glb))
    return loc


if __name__ == '__main__':

    n = 100

    data = numpy.random.logistic(size=(n, 2))

    seq = hess_sequence(n, oracle=oracle, fast=True)

    x, y = zip(*[data[i] for i in seq + [seq[0]]])

    plt.title('PEQNP - www.peqnp.science')
    plt.plot(x, y, 'k-')
    plt.plot(x, y, 'r.')
    plt.savefig('tsp.png')
```

# Real Time TSP with HESS

A bouncing balls GUI with the realtime power of HESS.

```python
import random
from tkinter import *

from peqnp import *


class Ball:
    def __init__(self, idx):
        self.idx = idx
        self.shape = canvas.create_oval(0, 0, SIZE, SIZE, fill='red')
        self.speed_x = random.randint(1, 10)
        self.speed_y = random.randint(1, 10)
        self.active = True
        self.move_active()

    def ball_update(self):
        canvas.move(self.shape, self.speed_x, self.speed_y)
        pos = canvas.coords(self.shape)
        if pos[2] >= WIDTH or pos[0] <= 0:
            self.speed_x *= -1
        if pos[3] >= HEIGHT or pos[1] <= 0:
            self.speed_y *= -1

    def move_active(self):
        if self.active:
            self.ball_update()
            tk.after(10, self.move_active)

    @property
    def position(self):
        pos = canvas.coords(self.shape)
        return complex(pos[2] - SIZE // 2, pos[3] - SIZE // 2)


def distance(seq):
    return sum(abs(balls[seq[i - 1]].position - balls[seq[i]].position) for i in range(len(balls)))


def update():
    seq = hess_sequence(len(balls), oracle=distance, fast=True)
    canvas.delete('lines')
    for i in range(len(seq)):
        x = balls[seq[i - 1]].position.real
        y = balls[seq[i - 1]].position.imag
        z = balls[seq[i]].position.real
        w = balls[seq[i]].position.imag
        canvas.create_line(x, y, z, w, fill="white", tags='lines')
    tk.after(10, update)


if __name__ == '__main__':
    WIDTH = 640
    HEIGHT = 480
    SIZE = 30
    N = 10

    tk = Tk()
    tk.title('PEQNP - Realtime TSP with HESS')
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    balls = []

    for i in range(N):
        balls.append(Ball(i))

    tk.after(10, update)

    tk.mainloop()
```