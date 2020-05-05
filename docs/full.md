# Full System

The PEQNP System include the HESS algorithm, that is a Universal Black Box Optimizer, the Diophantine and MIP Solvers.

# Partial Latin Hyper Cubes with Tensors

A multi - dimensional latin square with an empty element.

```python
import numpy as np
import peqnp as pn

if __name__ == '__main__':

    n = 6
    m = 3

    pn.engine((n + 1).bit_length())

    X = pn.tensor(dimensions=m * [n])
    Y = pn.vector(size=n ** m)

    pn.apply_single(Y, lambda k: 1 <= k <= n)

    t = np.empty(shape=n ** m, dtype=pn.Entity)
    for k, idx in enumerate(pn.hyper_loop(m, n)):
        t[k] = X[idx](0, Y[k])
    t = t.reshape(m * [n])

    for k in range(n):
        pn.all_different(t[k])
        pn.all_different(t.T[k])
        for l in range(n):
            pn.all_different(t[k][l])
            pn.all_different(t.T[k][l])

    for idx in pn.hyper_loop(m - 1, n):
        s = t
        for k in idx:
            s = s[k]
            pn.all_different(s)
            pn.all_different(s.T)

    if pn.satisfy(turbo=True, log=True):
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

import peqnp as pn


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
    seq = pn.hess_sequence(len(balls), oracle=distance)
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
