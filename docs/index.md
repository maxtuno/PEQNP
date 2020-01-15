# The PEQNP System

For more info visit [www.peqnp.science](http://www.peqnp.science) and [Source Codes](https://github.com/maxtuno/PEQNP) and [Documentation](https://peqnp.readthedocs.io).

# Introduction

The PEQNP System its a automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3.

# Installation

```python
pip3 install PEQNP --upgrade
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

+, -, *, /, **, %, &, |, ^, ==, =, <, <=, >, >=.

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

