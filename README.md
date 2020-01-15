# PEQNP
General Constrained Diophantine Equation Solver
# HESS 
Hyper Expoential Space Sorting an Universal Black Box Optimizer
# DEIDOS COVENANT 
A extremely fast algorithm to get all solutions of a Sum Subset Problem. (with 3sort Algorithm)
# SLIME 4
A Free World Class High Performance SAT Solver

[![Downloads](https://pepy.tech/badge/peqnp)](https://pepy.tech/project/peqnp)

To install the latest version:

    pip3 install PEQNP --upgrade
    
Longest Common Pattern Example (Longest Common Sequence with Permutations):

    import numpy as np
    from peqnp import *
    
    m, n = 7, 15

    mapping = {1: '-', n: 'A', n ** 2: 'C', n ** 3: 'T', n ** 4: 'G'}

    t, S = 0, []
    for i in range(m):
        S.append([n ** i for i in np.random.randint(1, 5, size=n)])
        t = max(t, np.sum(S[-1]))
        print(''.join([mapping[s] for s in S[-1]]))

    opt = 1
    while True:
        engine(int(t).bit_length())

        X = []
        for s in S:
            X.append(np.asarray(subset(s, k=n, empty=1)))

        apply_dual(X, lambda a, b: np.sum(a) == np.sum(b) > opt)

        if satisfy(turbo=True):
            print()
            opt = np.sum(X[-1])
            for x in X:
                print(''.join([mapping[int(x[i])] for i in range(n)]))
        else:
            break
            
Output:

    CCTAACGGAGCTATTACAAT
    GCCTAGGCGTCTCCTACAAT
    TGTCGGATGGCATCCAGTGA
    TCTCTGTGCGGGTAAGACAC
    GTAGAGGCTAGTTTTGGACC
    
    --TA--G--GC------AAT
    G--T-G-C------TA-AA-
    -------TG-CAT--A--GA
    --T-TG-G-----A--ACA-
    --A-A-G--A-T--TG---C
    
    CCTAAC-G-G---T------
    GCCTA--CGT-----A----
    ---C-GATG-C-TC-A----
    TCTC-G--CG---AA-----
    --AGA--C---T--T-G-CC
    
    C-----GG-G--A------T
    G--T-GG------C-A----
    T---G----G-A-C----G-
    ----TG----G---AG-C--
    -----G-CTA-----GG---
    
    C-T---GG-G-T-T---AAT
    G--TAGG--T-T--TAC---
    TG-CG-AT----T--AGT--
    TCT-T-T---GG---GA-A-
    GT--AGG--A--TTT----C
    
    --T---GG-GCT-T-AC--T
    G--T-GG--T-T-C--C-AT
    TGT-G-AT--C---C--TG-
    TCT-T-----GGT--G-CA-
    G---A-GC--GTTTT---C-
    
    C-T---GG-G-T-TTAC-A-
    GC-TAGG--T-TC-TA----
    TGTC---T-G-A-C-A-TG-
    TCTCT--G-GG-TAA-----
    -----GGC-AGTTTT--AC-
    
    --T--CGG-GCTATT----T
    GCCTAGG--T-T--T----T
    T-TC---TGGC-T---GT-A
    TCTCTGT--G-GT-----A-
    -----G-CTAGTTTTG---C
    
    --TA--GG-GCT-TTAC-AT
    ---TAGG-GT-T-CT-CAAT
    T-T--GATG--ATCC-GT-A
    TCT-T-T---GGTAAGA--C
    GTAGAG---A-TTTT---CC
    
    CCTAA-GGAG-T-TT-CA-T
    ---TAGGCGT-T-CTACAAT
    T-TCG-ATGGCAT-CA-T-A
    T-TCTGTGC-G-TAA-A-AC
    G-AGA--CTA-TTTTG-ACC

More Examples https://github.com/maxtuno/PEQNP

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

#### version 0.1.40
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
- Add the HESS folder with NATIVE and variate implementations of the HESS algorithm to solve (approximate) MAXSAT, HCP, CVRP and the Hyper Loop Algorithm. 
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
 
