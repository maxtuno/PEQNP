# MIP

Currently exist a module for Mixed Integer Programming can solve linear constraints on standard form: 

    expresion [<=, >=, ==] real

# The knapsack problem. 

```python
import random
from peqnp import *

if __name__ == '__main__':
    n = 10

    values = [random.random() for _ in range(n)]
    profit = [random.random() for _ in range(n)]

    capacity = sum(random.sample(values, k=n // 2))

    engine()
    
    # Declare a vector s linear variables
    selects = vector(is_mip=True, size=n)
    
    # All variables are binary
    apply_single(selects, lambda x: x <= 1)
    
    # Apply the dot product on variables and values and do constraints
    assert dot(values, selects) <= capacity
    
    # maximize the objective
    opt = maximize(dot(profit, selects))
    
    # get a separates copy solution, the variables continue by reference and can be affected by operations.
    slots = list(map(int, selects))
    
    # show solution
    print('PROFIT  : {} vs {}'.format(dot(profit, slots), opt))
    print('VALUES  : {} <= {}'.format(dot(values, slots), capacity))
    print('SELECT  : {}'.format(slots))
```

# Simple Example

```python
from peqnp import *

if __name__ == '__main__':

    engine()

    x1 = linear()
    x2 = linear()
    x3 = linear()
    x4 = linear(is_real=True)

    assert x1 + 2.1 * x3 <= 700.1
    assert 2.1 * x2 - 0.8 * x3 <= 0
    assert x2 - 2 * x3 + x4 >= 1.5
    assert x2 + x2 + x3 + 0.1 * x4 == 10.123

    assert x1 <= 10
    assert x1 >= 10
    assert x2 <= 20

    opt = maximize(x1 + x2 + 2 * x3 - 2 * x4)

    print(opt, x1, x2, x3, x4)
```

```
-16.45999999999998 10 0 8 21.22999999999999
```
