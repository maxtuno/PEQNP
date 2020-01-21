# NP-Complete Problems

NP-complete problem, any of a class of computational problems for which no efficient solution algorithm has been found. Many significant computer-science problems belong to this class—e.g., the traveling salesman problem, satisfiability problems, and graph-covering problems.

# Satisfiability

Study of boolean functions generally is concerned with the set of truth assignments (assignments of 0 or 1 to each of the variables) that make the function true.

```python
import functools
import operator

from peqnp import *  

n, m, cnf = 10, 24, [[9, -5, 10, -6, 3],
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
engine(bits=2)

# Declare an integer of n-bits, each ith-bits is one ith-literal on the model.
x = integer(bits=n)

# For each clause ensure that that one of the lierals are true.
for cls in cnf:
    assert functools.reduce(operator.or_, (switch(x, abs(lit) - 1, neg=lit > 0) for lit in cls)) > 0

# Get only one solution or UNSAT.
# The turbo parameter, say to SLIME4 SAT Solver, that make a full simplification, 
# then the internal structure of the problem is destroyed is more fast for one solution problems.
if satisfy(turbo=True):
    print('SAT')
    print(' '.join(map(str, [(i + 1) if b else -(i + 1) for i, b in enumerate(x.binary)])) + ' 0')
else:
    print('UNSAT')
```

```python
SAT
-1 2 -3 4 5 -6 7 8 -9 -10 0
```

With SLIME 4 SAT Solver

```python
from peqnp import *

print(slime4('instance.cnf'))
print(slime4('sat.cnf', 'sat.mod'))
print(slime4('unsat.cnf', 'unsat.mod', 'unsat.proof'))
```

# 0-1 Integer Programming

Input: Integer matrix \(C\) and integer vector \(d\)

Property: There exist a 0-1 vector \(x\) sich that \(Cx=d\).

```python
import numpy as np
from peqnp import *

# the dimensions of the matrix
n, m = 10, 5

# The matrix
cc = np.random.randint(0, 100, size=(n, m))
# Ensure that solution exist (for gen some interesting example)
d = np.dot(cc, np.random.randint(0, 2, size=(m,)))

print(cc)
print(d)

# Setup the engine with the bits of the sum of all values of the matrix, this ensure that the entire problem is well represented represented on the system.
engine(bits=int(np.sum(cc)).bit_length())

# Declare a m-sized vector
xs = vector(size=m)

# All element of the vector are binaries, i.e. 0 or 1
all_binaries(xs)

# The main constrain for the problem (there is a one of the Karp's 21 NP-complete problems https://people.eecs.berkeley.edu/~luca/cs172/karp.pdf)
assert (np.dot(cc, xs) == d).all()

# Get the first solution with turbo
# very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
# only one solution is possible, because the internal structure of the problem is destroyed
if satisfy(turbo=True):
    print(xs)
    print(np.dot(cc, xs))
else:
    print('Infeasible...')
``` 

```python
[[72 36 46 70 22]
 [57 35 37 99 60]
 [35 87 81 48 74]
 [12 33  8 73 89]
 [28 51 12 62 91]
 [71 65 69 87  2]
 [ 4  8 23 58 84]
 [93 88 71 50 78]
 [34 20 57  0 24]
 [83 95 37 61 50]]
[108  92 122  45  79 136  12 181  54 178]
[1, 1, 0, 0, 0]
[108 92 122 45 79 136 12 181 54 178]
``` 

# Clique

Input: Graph \(G\), positive integer \(k\)

Property: \(G\) has a set of mutually adjacent nodes.

```python
from peqnp import *

# Ths bits of the clique to search
k = 3

# Get the graph and the dimension for the graph
n, matrix = 5, [(1, 0), (0, 2), (1, 4), (2, 1), (4, 2), (3, 2)]

# Ensure the problem can be represented
engine(bits=k.bit_length())

# Declare an integer of n-bits
bits = integer(bits=n)

# The bits integer have "bits"-active bits, i.e, the clique has "bits"-elements
assert sum(switch(bits, i) for i in range(n)) == k

# This entangle all elements that are joined together
for i in range(n - 1):
    for j in range(i + 1, n):
        if (i, j) not in matrix and (j, i) not in matrix:
            assert switch(bits, i) + switch(bits, j) <= 1

# Get the first solution with turbo
# very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
# only one solution is possible, because the internal structure of the problem is destroyed
if satisfy(turbo=True):
    print(k)
    print(' '.join([str(i) for i in range(n) if not bits.binary[i]]))
else:
    print('Infeasible ...')
```

```python
3
0 1 2
```

# The Sum Subset Problem

```python
from peqnp import *

# Get the target and data 
t, universe = 12, [2, 3, 5, 7, 11]

# Declare an engine with same bits of the target.
engine(bits=t.bit_length())

# Get all possible subsets for the data
bits, subset = subsets(universe)

# Ensure that this subset sum the target.
assert sum(subset) == t

# Solve
if satisfy(turbo=True):
    solution = [universe[i] for i in range(len(universe)) if bits.binary[i]]
    print(sum(solution), solution)
else:
    print('Infeasible ...')
```

```python
12 [5, 7]
```

# Vertex Cover

```python
from peqnp import *

# Get the graph and dimension, and the bits of the cover.
n, graph, vertex, k = 5, [(1, 0), (0, 2), (1, 4), (2, 1), (4, 2), (3, 2)], [0, 1, 2, 3, 4], 3

# Ensure the problem can be represented
engine(bits=n.bit_length() + 1)

# An integer with n-bits to store the indexes for the cover
index = integer(bits=n)

# This entangled the all possible covers
for i, j in graph:
    assert switch(index, vertex.index(i), neg=True) + switch(index, vertex.index(j), neg=True) >= 1

# Ensure the cover has bits k
assert sum(switch(index, vertex.index(i), neg=True) for i in vertex) == k

# Get the first solution with turbo
# very fast but destructive, this force a SLIME 4 SAT Solver do a full simplification,
# only one solution is possible, because the internal structure of the problem is destroyed
if satisfy(turbo=True):
    opt = sum(index.binary)
    print('p bits {}'.format(opt))
    print(' '.join([str(vertex[i]) for i in range(n) if index.binary[i]]))
    print()
else:
    print('Infeasible ...')
```

```
p size 3
0 3 4
```