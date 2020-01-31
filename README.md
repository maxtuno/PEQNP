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
    
Latin Hyper Cubes:

    import numpy as np
    from peqnp import *
    
    n = 6
    m = 3
    
    engine(n.bit_length() + 1)
    
    Y = vector(size=n ** m)
    
    apply_single(Y, lambda k: k < n)
    
    Y = np.reshape(Y, newshape=(m * [n]))
    
    for i in range(n):
        all_different(Y[i])
        all_different(Y.T[i])
        for j in range(n):
            all_different(Y[i][j])
            all_different(Y.T[i][j])
    
    for idx in hyper_loop(m - 1, n):
        s = Y
        for i in idx:
            s = s[i]
            all_different(s)
            all_different(s.T)
    
    if satisfy(turbo=True, boost=True, log=True):
        y = np.vectorize(int)(Y).reshape(m * [n])
        print(y)
        print(80 * '-')
    else:
        print('Infeasible ...')

Output:

     [[[4 1 5 2 3 0]
       [1 5 2 4 0 3]
       [5 2 3 0 4 1]
       [2 4 0 3 1 5]
       [0 3 4 1 5 2]
       [3 0 1 5 2 4]]
     
      [[5 0 4 3 1 2]
       [0 4 3 5 2 1]
       [4 3 2 1 5 0]
       [3 5 1 2 0 4]
       [2 1 0 4 3 5]
       [1 2 5 0 4 3]]
     
      [[0 4 3 5 2 1]
       [5 0 4 3 1 2]
       [3 5 1 2 0 4]
       [4 3 2 1 5 0]
       [1 2 5 0 4 3]
       [2 1 0 4 3 5]]
     
      [[1 5 2 4 0 3]
       [4 1 5 2 3 0]
       [2 4 0 3 1 5]
       [5 2 3 0 4 1]
       [3 0 1 5 2 4]
       [0 3 4 1 5 2]]
     
      [[3 2 1 0 4 5]
       [2 3 0 1 5 4]
       [0 1 5 4 3 2]
       [1 0 4 5 2 3]
       [4 5 3 2 1 0]
       [5 4 2 3 0 1]]
     
      [[2 3 0 1 5 4]
       [3 2 1 0 4 5]
       [1 0 4 5 2 3]
       [0 1 5 4 3 2]
       [5 4 2 3 0 1]
       [4 5 3 2 1 0]]]
    
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

#### version 0.3.0
- Fix MIP module crash.

#### version 0.2.8
- Better memory management from python native code.
- This increases the resolution speed considerably.

#### version 0.2.5
- SLIME 4 Updated to SAT RACE Performance.
- Add the TENSOR object.
- Examples on use of tensor.

#### version 0.2.4
- Improve HESS algorithm, add two parameters fast (now default), and cycles.
- Add HYPER LOOP algorithm a nested for loop from www.PEQNP.science. 
- Now is possible activate the BOOST Heuristic on SLIME 4 with the parameter boost=True. ref: https://helda.helsinki.fi/handle/10138/306988 (SLIME)
- Several examples for test the new features. v2-boost (folder)

#### version 0.2.3
- Several Improvements on Rationals and Gaussian Integers Sub Module
- Add several examples on new features.

#### version 0.2.2
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
 