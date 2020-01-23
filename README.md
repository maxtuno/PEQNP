# PEQNP

The PEQNP System its a automatic CNF encoder and SAT Solver for General Constrained Diophantine Equations and NP-Complete Problems, full integrated with Python 3.

# SLIME 4
A Free World Class High Performance SAT Solver

# HESS 
Hyper Expoential Space Sorting an Universal Black Box Optimizer

# DEIDOS COVENANT 
A extremely fast algorithm to get all solutions of a Sum Subset Problem.

# 3 Sort 

A O(floor(n^2)/4) and O(1) memory sorting algorithm. 

[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)

To install the latest version:

    pip install PEQNP --upgrade
    
Schur Triples problem: (Strong NP-Complete):

    # ref: https://cstheory.stackexchange.com/questions/16253/list-of-strongly-np-hard-problems-with-numerical-data
    
    import random
    
    from peqnp import *
    
    bits = 7
    size = 3 * 3
    
    triplets = []
    while len(triplets) < size:
        a = random.randint(1, 2 ** bits)
        b = random.randint(1, 2 ** bits)
        if a != b and a not in triplets and b not in triplets and a + b not in triplets:
            triplets += [a, b, a + b]
    triplets.sort()
    print(triplets)
    print()
    
    engine(bits=max(triplets).bit_length())
    
    xs, ys = permutations(triplets, size)
    
    for i in range(0, size, 3):
        assert ys[i] + ys[i + 1] == ys[i + 2]
    
    if satisfy(turbo=True):
        for i in range(0, size, 3):
            print('{} == {} + {}'.format(ys[i + 2], ys[i], ys[i + 1]))
    else:
        print('Infeasible ...')

            
Output:

    [7, 9, 19, 20, 32, 48, 53, 59, 67, 76, 82, 84, 85, 100, 103, 108, 109, 112, 113, 115, 116, 119, 125, 132, 144, 148, 172, 192, 201, 218]
    
    132 == 112 + 20
    85 == 53 + 32
    192 == 108 + 84
    201 == 119 + 82
    144 == 125 + 19
    172 == 59 + 113
    218 == 115 + 103
    148 == 48 + 100
    76 == 67 + 9
    116 == 7 + 109

    
More Examples https://github.com/maxtuno/PEQNP/tree/master/examples

More info:

PEQNP Home
www.peqnp.science

Twitter Account
https://twitter.com/maxtuno

Youtube Channel
https://www.youtube.com/channel/UCFlk1dUYLKtymcoMScdynNA

Facebook Page
https://www.facebook.com/PEQNP-104747814228901

Documentation
https://peqnp.readthedocs.io

### version 0.2.2
- Add beta support for Mixed Integer Programming

#### version 0.2.0
- A considerable improvement on performance.
- Fix several edge conditions bugs.
- Add the operations <<, >>.
- Complete Revision of Examples.

#### version 0.1.41
- Add beta support for rational numbers
- Add documentation

#### version 0.1.39
- Add performance improvement on solving.
- Add at_most_k, sqrt functions.
- Fix some bugs on gaussian integers, and add Gaussian Factorization example.
- Fix some edge condition bugs.
- Add several examples more.
- Add simple documentation for the STDLIB.

#### 1-8-2020
- Add the HESS folder with NATIVE and variate implementations of the HESS algorithm to sl (approximate) MAXSAT, HCP, CVRP and the Hyper Loop Algorithm. 
- SLIME4 is now compile on this project.
- Add DEIDOS COVENANT Algorithm, to get all solutions of a Sum Subset Problem.
- Add the longest common pattern (permutation) problem example.

#### version 0.1.38
- Add normalize parameter to satisfy, this normalize integers from [2 ** (bits - 1), 2 ** bits - 1] and add a related example.

#### version 0.1.37
- Add beta support for Gaussian Integers, and related examples.

#### version 0.1.35
- Add index function the inverse of element function, its the equivalent to vector[index] == element.
- Add matrix equation example.

#### version 0.1.34
- Add functions matrix_permutation, permutations, combinations
- Update the Schur Triples example with permutations function.
- Add model_path to satisfy function.

#### version 0.1.33
- Add the "Min Vertex Cover" example.
- Add the function "index = element(item, data)" this ensure that the element item is in data on the position index.
- Add example for "element" function.

#### version 0.1.32
- Add the function slime4(cnf_path, model_path, proof_path) this call to SLIME 4 SAT Solver directly.

#### version 0.1.31
- Fix URL on SLIME log.

#### version 0.1.30
- Add support for android, ARM C++ compilation.
- Add version() function that return the current version of the system.
- Add proof_path parameter to satisfy(), this generate the DRUP-PROOF of the problem if its is unsatisfiable.
 
