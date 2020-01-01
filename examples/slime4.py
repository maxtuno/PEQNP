from peqnp import *

if __name__ == '__main__':

    print(slime4('pq.cnf'))
    print(slime4('sat.cnf', 'sat.mod'))
    print(slime4('unsat.cnf', 'unsat.mod', 'unsat.proof'))

