"""
The standard high level library for the PEQNP system.
"""

from .solver import *

csp = None
variables = []


def engine(bits=None, deepness=None):
    """
    Initialize and reset the internal state of solver engine.
    :param bits: The size 2 ** bits - 1 of solving space.
    :param deepness: The scope for the exponential variables bits / 2 by default.
    :return:
    """
    global csp
    csp = CSP(bits, deepness)


def version():
    """
    Print the current version of the system.
    :return:
    """
    print('PEQNP - 0.1.31 - 31-12-2019')


def integer(key=None, bits=None):
    """
    Correspond to an integer of name key, and size bits.
    :param key: The name of variable, appear on CNF when cnf_path is setting on satisfy().
    :param bits: The bits size of the integer.
    :return: An instance of Integer.
    """
    global variables
    variables.append(csp.int(key=key, size=bits))
    return variables[-1]


def constant(value=None, bits=None):
    """
    Correspond to an constant of value with size bits.
    :param bits: The bits size of the constant.
    :param value: The value that represent the constant.
    :return: An instance of Constant.
    """
    global variables
    variables.append(csp.int(size=bits, value=value))
    return variables[-1]


def satisfy(solve=True, turbo=False, log=False, assumptions=[], cnf_path='', proof_path=''):
    """
    Find a model for the current problem.
    :param solve: This indicate if the instance can be solved or not, its use in conjunction with cnf_path.
    :param turbo: This make a simplification of the model, is more fast to solve, but destroy the internal structure of the problem, need regenerate, and gent only one solution.
    :param log: Shot the log for the SLIME SAT Solver.
    :param assumptions: A low level interrupt on the solver, this take a list with literals assumed true, and add to the hig level model.
    :param cnf_path: The path for the CNF representation of the problem, None by default and is not generated.
    :param proof_path: The path for the CNF DRUP-PROOF of the problem if this is unsatisfiable, None by default and is not generated.
    :return: True if SATISFIABLE else False
    """
    return csp.to_sat(variables, solve=solve, turbo=turbo, log=log, assumptions=assumptions, cnf_path=cnf_path, proof_path=proof_path)


def subsets(universe, k=None, key=None):
    """
    Generate all subsets for an specific universe of data.
    :param universe: The universe of data.
    :param k: The cardinality of the subsets.
    :param key: The name os the binary representation of subsets.
    :return: (binary representation of subsets, the generic subset representation)
    """
    global variables
    bits = csp.int(key=key, size=len(universe))
    variables.append(bits)
    if k is not None:
        assert sum(csp.zero.iff(-bits[i], csp.one) for i in range(len(universe))) == k
    subset_ = [csp.zero.iff(-bits[i], universe[i]) for i in range(len(universe))]
    variables += subset_
    return bits, subset_


def subset(data, k, empty=None):
    """
    An operative structure (like integer ot constant) that represent a subset of at most k elements.
    :param data: The data for the subsets.
    :param k: The maximal size for subsets.
    :param empty: The empty element, 0, by default.
    :return: An instance of Subset.
    """
    global csp, variables
    subset_ = csp.subset(k, data, empty)
    variables += subset_
    return subset_


def vector(key=None, bits=None, size=None):
    """
    A vector of integers.
    :param key: The generic name for the array this appear indexed on cnf.
    :param bits: The bit size for each integer.
    :param size: The size of the vector.
    :return: An instance of Vector.
    """
    global csp, variables
    array_ = csp.array(key=key, size=bits, dimension=size)
    variables += array_
    return array_


def matrix(key=None, bits=None, dimensions=None):
    """
    A matrix of integers.
    :param key: The generic name for the array this appear indexed on cnf.
    :param bits: The bit size for each integer.
    :param dimensions: An tuple with the dimensions for the array (n, m).
    :return: An instance of Matrix.
    """
    global variables
    matrix_ = []
    for i in range(dimensions[0]):
        row = []
        for j in range(dimensions[1]):
            variables.append(integer(key='{}_{}_{}'.format(key, i, j) if key is not None else key, bits=bits))
            row.append(variables[-1])
        matrix_.append(row)
    return matrix_


def permutations(args, n):
    """
    This generate the permutations for an square matrix.
    :param args: The matrix of data.
    :param n: The dimension for the square nxn-matrix.
    :return: An tuple with (index for the elements, the elements that represent the indexes)
    """
    global csp, variables
    xs = vector(size=n)
    ys = vector(size=n)
    csp.apply(xs, single=lambda x: x < n)
    csp.apply(xs, dual=lambda a, b: a != b)
    if isinstance(args[0], list):
        csp.indexing(xs, ys, csp.flatten(args))
    else:
        csp.indexing(xs, ys, args)
    return xs, ys


def all_binaries(args):
    """
    This say thay, the vector or matrix of integer are all binaries.
    :param args: The matrix or vector of integers.
    :return:
    """
    global csp
    if isinstance(args[0], list):
        csp.apply(csp.flatten(args), single=lambda arg: arg <= 1)
    else:
        csp.apply(args, single=lambda arg: arg <= 1)


def switch(arg, ith, neg=False):
    """
    This conditionally flip the internal bit for an integer.
    :param arg: The integer.
    :param ith: Indicate the ith bit.
    :param neg: indicate if the condition is inverted.
    :return: 0 if the uth bit for the argument collapse to true else return 1, if neg is active exchange 1 by 0.
    """
    global csp
    return csp.zero.iff(-arg[ith] if neg else arg[ith], csp.one)


def one_of(args, key=None):
    """
    This indicate that at least one of the instruction on the array is active for the current problem.
    :param args: A list of instructions.
    :param key: The name for the bits relative to vector that are active on the operation.
    :return: The entangled structure.
    """
    global csp
    bits = csp.int(key, size=len(args))
    assert sum(csp.zero.iff(bits[i], csp.one) for i in range(len(args))) == 1
    return sum(csp.zero.iff(bits[i], args[i]) for i in range(len(args)))


def factorial(arg):
    """
    The factorial for the integer.
    :param arg: The integer.
    :return: The factorial.
    """
    global csp
    return csp.factorial(arg)


def sigma(f, i, n):
    """
    The Sum for i to n, for the lambda function f,
    :param f: A lambda function with an standard int parameter.
    :param i: The start for the Sum, an standard int.
    :param n: The integer that represent the end of the Sum.
    :return: The entangled structure.
    """
    global csp
    return csp.sigma(f, i, n)


def pi(f, i, n):
    """
    The Pi for i to n, for the lambda function f,
    :param f: A lambda function with an standard int parameter.
    :param i: The start for the Pi, an standard int.
    :param n: The integer that represent the end of the Pi.
    :return: The entangled structure.
    """
    global csp
    return csp.pi(f, i, n)


def dot(xs, ys):
    """
    The dot product of two compatible Vectors.
    :param xs: The fist Vector
    :param ys: The second Vector
    :return: The dot product.
    """
    global csp
    return csp.dot(xs, ys)


def mul(xs, ys):
    """
    The elementwise product of two Vectors.
    :param xs: The fist Vector
    :param ys: The second Vector
    :return: The product.
    """
    global csp
    return csp.mul(xs, ys)


def apply_single(args, f):
    """
    A sequential operation over a Vector.
    :param args: the Vector.
    :param f: The lambda function of one integer variable.
    :return: The entangled structure.
    """
    global csp
    csp.apply(args, single=f)


def apply_dual(args, f):
    """
    A cross operation over a Vector.
    :param args: the Vector.
    :param f: The lambda function of two integer variables.
    :return: The entangled structure.
    """
    global csp
    csp.apply(args, dual=f)


def all_different(args):
    """
    The all different global constraint.
    :param args: A vector of integers.
    :return:
    """
    global csp
    csp.apply(args, dual=lambda x, y: x != y)


def flatten(args):
    """
    Flatten a matrix into list.
    :param args: The matrix.
    :return: The entangled structure.
    """
    global csp
    return csp.flatten(args)


def oo():
    """
    The infinite for rhe system, the maximal value for the current engine.
    :return: 2 ** bits - 1
    """
    global csp
    return csp.oo
