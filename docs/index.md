# The System

For more info visit [www.peqnp.science](http://www.peqnp.science) and [Source Codes](https://github.com/maxtuno/PEQNP) and [Documentation](https://peqnp.readthedocs.io).

# Introduction

The PEQNP System its a automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3.

# Installation
[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)
```python
pip install PEQNP --upgrade
```

A simple example its the factorization of RSA numbers.
    
### With Integers:    
    
```python
from peqnp import *

rsa = 3007

engine(rsa.bit_length())

p = integer()
q = integer()

assert p * q == rsa

while satisfy():
    print(p, q)
```
output:
```python
3007 1
31 97
1 3007
97 31
```

# Native Operations

On PEQNP all elements are integers and relations on this integers, this relations are at bit level or arithmetic level.

## Supported Operations

+, -, *, /, \*\*, pow_mod, %, &, |, ^, ==, =, <, <=, >, >=, <<, >>.

## Integers

All integers live on \(\mathbb{N}_{2^{bits} - 1}\) and always positives, i.e. for two integer \(x, y\) the operation, \(x - y\) take all possibilities such that \(x - y >= 0\).         

## The Mantra

First is needed import all PEQNP system.

```python
from peqnp import *
```

Define the data and constants.

```python
bits = 10
```

Next initialize the engine.

```python
engine(bits=10)
```

Declare the variables.

```python
x = integer()
```

Add constrains.

```python
assert x < 10
```

Solve the problem.

```python
while satisfy():
    print(x)
```

# A Full Example

### multiset reconstruction by differences

```python
import time
import random

from peqnp import *

"""
Given a sorted multiset, their differences and one tip: an element and position for only one arbitrary element, is possible recovery the original multiset?
"""

def generator(n, max_val):
    return sorted([random.randint(1, max_val) for _ in range(n)])


def differences(lst):
    return [abs(lst[i] - lst[i - 1]) for i in range(1, len(lst))]


if __name__ == '__main__':

    for n in range(1, 100):

        m = random.randint(1, n ** 2)

        original = generator(n, m)
        diffs = differences(original)

        print()
        print('N, M         : {}, {}'.format(n, m))
        print('DIFFERENCES  : {}'.format(diffs))
        print('ORIGINAL     : {}'.format(original))

        # only one tip
        ith = random.choice(range(n))
        tip = original[ith]

        # init timer
        ini = time.time()

        # Empirical bits necessarily to solve the problem.
        engine(sum(diffs).bit_length() + 4)

        # Declare a n-vector of integer variables to store the solution.
        x = vector(size=n)

        # The tip is on x at index ith
        assert tip == index(ith, x)

        # The i-th element of the instance is the absolute difference of two consecutive elements
        for i in range(n - 1):
            assert x[i] <= x[i + 1]
            assert index(i, diffs) == x[i + 1] - x[i]

        # Solve the problem for only one solution.
        if satisfy(turbo=True):
            o = [abs(x[i + 1] - x[i]) for i in range(n - 1)]
            c = 100 * len(set(map(int, x)).intersection(set(original))) / len(set(original))
            print('SOLVED       : {}'.format(x))
            print('COINCIDENCES : {}%'.format(c))
            if o == diffs:
                print('OK! - {}s'.format(time.time() - ini))
            else:
                print('NOK! - {}s'.format(time.time() - ini))
                raise Exception('ERROR!')
            if c != 100:
                raise Exception('Hypothesis Fail - 100%')
```
