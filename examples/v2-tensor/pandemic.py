"""
Copyright (c) 2012-2020 PEQNP. all rights reserved. contact@peqnp.science

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from matplotlib.lines import Line2D
from peqnp import *
import numpy as np
import matplotlib.pyplot as plt

"""
Are Several infectious outbreaks with different severity, 
we have a number of centers capable of attending to these patients, 
we have a measure of the waiting time by center and severity,
the crisis needs to be resolved in the shortest possible time.
"""


def generate_instance(infections, centres, priorities, max_capacity=200, max_demand=10, max_time=15):
    a = np.random.randint(1, max_demand, size=infections)
    b = np.random.randint(0, priorities, size=infections)
    c = np.random.randint(max_capacity // 4, max_capacity, size=(centres, priorities))
    t = np.random.randint(1, max_time, size=(centres, priorities))
    D = np.random.uniform(-10, 10, size=(infections, 2))
    C = np.random.logistic(size=(centres, 2)) * 5
    return a, b, c, t, D, C


if __name__ == '__main__':

    infections, centres, priorities = 20, 10, 3

    # a: Number of infections by focus
    # b: Severity of each Infection
    # c: Severity by Center
    # t: Wait time for urgent care by Severity and Centers
    # D: Locations of infections
    # C: Location of Centers
    a, b, c, t, D, C = generate_instance(infections, centres, priorities)

    print(a)
    print(b)
    print(c)
    print(t)

    print(D)
    print(C)

    opt, dis = 0, 0
    while True:

        engine(16)

        X = tensor(dimensions=[infections, centres, priorities])

        s = constant(value=0)
        u = constant(value=0)

        # Maximize total number of people helped and minimize total time to solve the crisis and minizie distance ar centers from focus.
        for i in range(infections):
            for j in range(centres):
                for k in range(priorities):
                    if b[i] == k:
                        s += X[i, j, k](0, a[i])
                        u += X[i, j, k](0, (1000 // (t[j][k] + np.linalg.norm(D[i] - C[j]))))
                    else:
                        assert X[i, j, k](0, 0)

        # Optimality condition
        assert s > opt
        assert u >= dis

        # The limit for attended people is the capacity of the centers
        for k in range(priorities):
            for j in range(centres):
                assert sum(X[i, j, k](0, a[i]) for i in range(infections) if b[i] == k) <= c[j][k]

        # Consistence conditions

        for j in range(centres):
            for k in range(priorities):
                assert sum(X[i, j, k](0, 1) for i in range(infections)) <= 1

        for i in range(infections):
            for k in range(priorities):
                assert sum(X[i, j, k](0, 1) for j in range(centres)) <= 1

        for i in range(infections):
            for j in range(centres):
                assert sum(X[i, j, k](0, 1) for k in range(priorities)) <= 1

        # Optimize
        if satisfy(turbo=True, log=True, boost=True):
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)

            dx, dy = zip(*D)
            cx, cy = zip(*C)
            plt.scatter(dx, dy, c='r', s=a * 10)
            plt.scatter(cx, cy, c='g', s=c * 10)

            opt, dis = 0, 0
            s, r, o = 0, 0, 0
            for i in range(infections):
                for j in range(centres):
                    for k in range(priorities):
                        if X.binary[i][j][k]:
                            s += a[i]
                            r += t[j][k]
                            o += np.linalg.norm(D[i] - C[j])
                            print('{} INFECTIONS FROM {} WITH PRIORITY {} ATTENDED CENTER {} LOCATED AT {} WIT CAPACITY {} WAITING TIME {}'.format(a[i], i, j, k, np.linalg.norm(D[i] - C[j]), c[j][k], t[j][k]))
                            ax.add_line(Line2D([D[i][0], C[j][0]], [D[i][1], C[j][1]]))
                            opt += a[i]
                            dis += (1000 // (t[j][k] + np.linalg.norm(D[i] - C[j])))
            print()
            print('TOTAL DISTANCE IS {}'.format(o))
            print('TOTAL TIME TO SOLVE THE EMERGENCY IS {}'.format(r))
            print('TOTAL ATTENDED {} of {}'.format(s, sum(a)))
            print(80 * '-')
            plt.savefig('pandemic.png')
            plt.close()
            print('OPT | DIS : {}, {}'.format(opt, dis))
        else:
            break