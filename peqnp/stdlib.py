"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""

from .solver import *

csp = None
variables = []


def engine(bits=None, deepness=None):
    global csp
    csp = CSP(bits, deepness)


def integer(key=None, bits=None):
    global variables
    variables.append(csp.int(key=key, size=bits))
    return variables[-1]


def constant(bits=None, value=None):
    global variables
    variables.append(csp.int(key=str(value), size=bits, value=value))
    return variables[-1]


def satisfy(turbo=False):
    return csp.to_sat(variables, solve=True, turbo=turbo)


def subsets(universe, k=None):
    global variables
    bits = csp.int(size=len(universe))
    variables.append(bits)
    if k is not None:
        assert sum(csp.zero.iff(-bits[i], csp.one) for i in range(len(universe))) == k
    subset_ = [csp.zero.iff(-bits[i], universe[i]) for i in range(len(universe))]
    variables += subset_
    return bits, subset_


def subset(data, k, empty=None):
    global csp, variables
    subset_ = csp.subset(k, data, empty)
    variables += subset_
    return subset_


def vector(key=None, bits=None, size=None):
    global csp, variables
    array_ = csp.array(key=key, size=bits, dimension=size)
    variables += array_
    return array_


def matrix(key=None, bits=None, dimensions=None):
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
    global csp
    if isinstance(args[0], list):
        csp.apply(csp.flatten(args), single=lambda arg: arg <= 1)
    else:
        csp.apply(args, single=lambda arg: arg <= 1)


def switch(arg, ith, neg=False):
    global csp
    return csp.zero.iff(-arg[ith] if neg else arg[ith], csp.one)


def sign(arg):
    return 1 if arg >= 0 else -1


def one_of(args):
    global csp
    bits = csp.int(size=len(args))
    assert sum(csp.zero.iff(bits[i], csp.one) for i in range(len(args))) == 1
    return sum(csp.zero.iff(bits[i], args[i]) for i in range(len(args)))


def factorial(arg):
    global csp
    return csp.factorial(arg)


def sigma(f, i, n):
    global csp
    return csp.sigma(f, i, n)


def pi(f, i, n):
    global csp
    return csp.pi(f, i, n)


def dot(xs, ys):
    global csp
    return csp.dot(xs, ys)


def mul(xs, ys):
    global csp
    return csp.mul(xs, ys)


def apply_single(args, f):
    global csp
    csp.apply(args, single=f)


def apply_dual(args, f):
    global csp
    csp.apply(args, dual=f)


def all_different(args):
    global csp
    csp.apply(args, dual=lambda x, y: x != y)
