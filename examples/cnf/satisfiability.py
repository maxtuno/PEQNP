import functools
import operator

import peqnp.cnf as cnf

n, m, instance = 10, 24, [[9, -5, 10, -6, 3],
                          [6, 8],
                          [8, 4],
                          [-10, 5],
                          [-9, 8],
                          [-9, -3],
                          [-2, 5],
                          [6, 4],
                          [-2, -1],
                          [7, -2],
                          [-9, 4],
                          [-1, -10],
                          [-3, 4],
                          [7, 5],
                          [6, -3],
                          [-10, 7],
                          [-1, 7],
                          [8, -3],
                          [-2, -10],
                          [-1, 5],
                          [-7, 1, 9, -6, 3],
                          [-9, 6],
                          [-8, 10, -5, -4, 2],
                          [-4, -7, 1, -8, 2]]

# Initialize the engine with 2 bits
cnf.begin(bits=2, key='satisfiability')

# Declare an integer of n-bits, each ith-bits is one ith-literal on the model.
x = cnf.integer(bits=n)

# For each clause ensure that that one of the lierals are true.
for cls in instance:
    assert functools.reduce(operator.or_, (cnf.switch(x, abs(lit) - 1, neg=lit > 0) for lit in cls)) > 0

cnf.end({'x': x})

if cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
    print('SAT')
    print(' '.join(map(str, [(i + 1) if b else -(i + 1) for i, b in enumerate(x.binary)])) + ' 0')
else:
    print('UNSAT')
