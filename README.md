# PEQNP
General Constrained Diophantine Equation Solver

[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)

To install the latest version:

    pip3 install PEQNP --upgrade

Examples https://github.com/maxtuno/PEQNP

More info:

PEQNP Home
www.peqnp.science

Twitter Account
https://twitter.com/maxtuno

Youtube Channel
https://www.youtube.com/channel/UCFlk1dUYLKtymcoMScdynNA

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
 
