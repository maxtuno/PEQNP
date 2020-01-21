# Mixed Integer Programming

Currently exist a module for Mixed Integer Programming can solve constraints linear constraints on standard form: 

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