"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
The standard high level library for the PEQNP system.
"""

from .gaussian import Gaussian
from .linear import Linear
from .rational import Rational
from .solver import *

csp = None


def check_engine():
    if csp is None:
        print('The PEQNP System is not initialized...')
        exit(0)


def version():
    """
    Print the current version of the system.
    :return:
    """
    print('PEQNP Mathematical Solver from http://www.peqnp.com')
    try:
        import pixie
        print('PEQNP 2020 + SLIME 4 + PIXIE 1')
    except ImportError:
        print('PEQNP 2020 + SLIME 4')


def engine(bits=None, info=False):
    """
    Initialize and reset the internal state of solver engine.
    :param bits: The bits 2 ** bits - 1 of solving space.
    :param info: Return the info of the current system.
    :return:
    """
    global csp
    if bits is None:
        csp = CSP(0)
    else:
        csp = CSP(bits)
    if info:
        version()


def slime_cli(cnf_path, model_path='', proof_path=''):
    """
    Use directly the SLIME 4 SAT Solver.
    :param cnf_path: The cnf file to solve.
    :param model_path: The path to the model if SAT, optional.
    :param proof_path: The path for the DRUP-PROOF if UNSAT, optional.
    :return: A List with the model if SAT else an empty list.
    """
    import slime
    return slime.slime_cli(cnf_path, model_path, proof_path)


def integer(key=None, bits=None):
    """
    Correspond to an integer of name key, and bits bits.
    :param key: The name of variable, appear on CNF when cnf_path is setting on satisfy().
    :param bits: The bits of the integer.
    :return: An instance of Integer.
    """
    global csp
    check_engine()
    csp.variables.append(csp.int(key=key, size=bits))
    return csp.variables[-1]


def constant(value, bits=None):
    """
    Correspond to an constant of value with bits bits.
    :param bits: The bits bits of the constant.
    :param value: The value that represent the constant.
    :return: An instance of Constant.
    """
    global csp
    check_engine()
    csp.variables.append(csp.int(size=bits, value=value))
    return csp.variables[-1]


def satisfy(solve=True, turbo=False, log=False, assumptions=None, cnf_path='',
            model_path='', proof_path='', normalize=False):
    """
    Find a model for the current problem.
    :param solve: This indicate if the instance can be solved or not, its use in conjunction with cnf_path.
    :param turbo: This make a simplification of the model, is more fast to solve, but destroy the internal structure of the problem, need regenerate, and gent only one solution.
    :param log: Shot the log for the SLIME SAT Solver.
    :param assumptions: A low level interrupt on the solver, this take a list with literals assumed true, and add to the hig level model.
    :param cnf_path: The path for the CNF representation of the problem, None by default and is not generated.
    :param model_path: The path for the MODEL of the problem, None by default and is not generated.
    :param proof_path: The path for the CNF DRUP-PROOF of the problem if this is unsatisfiable, None by default and is not generated.
    :param normalize: Indicate to the system that normalize integers from [2 ** (bits - 1), 2 ** bits - 1].
    :return: True if SATISFIABLE else False
    """
    return csp.to_sat(csp.variables, solve=solve, turbo=turbo, log=log,
                      assumptions=assumptions, cnf_path=cnf_path,
                      model_path=model_path, proof_path=proof_path,
                      normalize=normalize)


def subsets(lst, k=None, key=None, complement=False):
    """
    Generate all subsets for an specific universe of data.
    :param lst: The universe of data.
    :param k: The cardinality of the subsets.
    :param key: The name os the binary representation of subsets.
    :param complement: True if include in return the complement.
    :return: (binary representation of subsets, the generic subset representation, the complement of subset if complement=True)
    """
    global csp
    check_engine()
    bits = csp.int(key=key, size=len(lst))
    csp.variables.append(bits)
    if k is not None:
        assert sum(
            csp.zero.iff(-bits[i], csp.one) for i in range(len(lst))) == k
    subset_ = [csp.zero.iff(-bits[i], lst[i]) for i in range(len(lst))]
    csp.variables += subset_
    if complement:
        complement_ = [csp.zero.iff(bits[i], lst[i]) for i in range(len(lst))]
        csp.variables += complement_
        return bits, subset_, complement_
    else:
        return bits, subset_


def subset(data, k, empty=None, complement=False):
    """
    An operative structure (like integer ot constant) that represent a subset of at most k elements.
    :param data: The data for the subsets.
    :param k: The maximal bits for subsets.
    :param empty: The empty element, 0, by default.
    :param complement: True if include in return the complement.
    :return: An instance of subset or (subset, complement) if complement=True.
    """
    global csp
    check_engine()
    if complement:
        subset_, complement_ = csp.subset(k, data, empty, complement=complement)
    else:
        subset_ = csp.subset(k, data, empty)
    csp.variables += subset_
    if complement:
        csp.variables += complement_
        return subset_, complement_
    return subset_


def vector(key=None, bits=None, size=None, is_rational=False, is_gaussian=False,
           is_mip=False, is_real=False):
    """
    A vector of integers.
    :param key: The generic name for the array this appear indexed on cnf.
    :param bits: The bit bits for each integer.
    :param size: The bits of the vector.
    :param is_rational: Indicate of is a Rational vector.
    :param is_gaussian: Indicate of is a Gaussian Integers vector.
    :param is_mip: Indicate of is a MIP vector.
    :param is_real: Indicate of is a MIP vector and is real or int.
    :return: An instance of vector.
    """
    global csp
    check_engine()
    if is_rational:
        return [rational() for _ in range(size)]
    if is_gaussian:
        return [gaussian() for _ in range(size)]
    if is_mip:
        lns = []
        for _ in range(size):
            lns.append(linear(is_real=is_real))
        return lns
    else:
        array_ = csp.array(key=key, size=bits, dimension=size)
        csp.variables += array_
    return array_


def matrix(key=None, bits=None, dimensions=None, is_mip=False, is_real=False):
    """
    A matrix of integers.
    :param key: The generic name for the array this appear indexed on cnf.
    :param bits: The bit bits for each integer.
    :param dimensions: An tuple with the dimensions for the array (n, m).
    :param is_mip: Indicate of is a MIP vector.
    :param is_real: Indicate of is a MIP vector and is real or int.
    :return: An instance of Matrix.
    """
    global csp
    check_engine()
    matrix_ = []
    for i in range(dimensions[0]):
        row = []
        lns = []
        for j in range(dimensions[1]):
            if is_mip:
                lns.append(linear(is_real=is_real))
                row.append(lns[-1])
            else:
                csp.variables.append(integer(key='{}_{}_{}'.format(key, i,
                                                                   j) if key is not None else key,
                                             bits=bits))
                row.append(csp.variables[-1])
        matrix_.append(row)
    return matrix_


def matrix_permutation(lst, n):
    """
    This generate the permutations for an square matrix.
    :param lst: The flattened matrix of data, i.e. a vector.
    :param n: The dimension for the square nxn-matrix.
    :return: An tuple with (index for the elements, the elements that represent the indexes)
    """
    global csp
    check_engine()
    xs = vector(size=n)
    ys = vector(size=n)
    csp.apply(xs, single=lambda x: x < n)
    csp.apply(xs, dual=lambda a, b: a != b)
    csp.indexing(xs, ys, lst)
    return xs, ys


def permutations(lst, n, key=None):
    """
    Entangle all permutations of bits n for the vector lst.
    :param lst: The list to entangle.
    :param n: The bits of entanglement.
    :return: (indexes, values)
    """
    check_engine()
    xs = vector(size=n, key=key)
    ys = vector(size=n)
    for i in range(n):
        assert element(ys[i], lst) == xs[i]
    apply_single(xs, lambda a: a < n)
    apply_dual(xs, lambda a, b: a != b)
    return xs, ys


def combinations(lst, n):
    """
    Entangle all combinations of bits n for the vector lst.
    :param lst: The list to entangle.
    :param n: The bits of entanglement.
    :return: (indexes, values)
    """
    check_engine()
    xs = vector(size=n)
    ys = vector(size=n)
    for i in range(n):
        assert element(ys[i], lst) == xs[i]
    return xs, ys


def all_binaries(lst):
    """
    This say that, the vector of integer are all binaries.
    :param lst: The vector of integers.
    :return:
    """
    check_engine()
    global csp
    csp.apply(lst, single=lambda arg: arg <= 1)


def switch(x, ith, neg=False):
    """
    This conditionally flip the internal bit for an integer.
    :param x: The integer.
    :param ith: Indicate the ith bit.
    :param neg: indicate if the condition is inverted.
    :return: 0 if the uth bit for the argument collapse to true else return 1, if neg is active exchange 1 by 0.
    """
    global csp
    check_engine()
    return csp.zero.iff(-x[ith] if neg else x[ith], csp.one)


def one_of(lst):
    """
    This indicate that at least one of the instruction on the array is active for the current problem.
    :param lst: A list of instructions.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    bits = csp.int(size=len(lst))
    assert sum(csp.zero.iff(bits[i], csp.one) for i in range(len(lst))) == 1
    return sum(csp.zero.iff(bits[i], lst[i]) for i in range(len(lst)))


def factorial(x):
    """
    The factorial for the integer.
    :param x: The integer.
    :return: The factorial.
    """
    global csp
    check_engine()
    return csp.factorial(x)


def sigma(f, i, n):
    """
    The Sum for i to n, for the lambda f f,
    :param f: A lambda f with an standard int parameter.
    :param i: The start for the Sum, an standard int.
    :param n: The integer that represent the end of the Sum.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    return csp.sigma(f, i, n)


def pi(f, i, n):
    """
    The Pi for i to n, for the lambda f f,
    :param f: A lambda f with an standard int parameter.
    :param i: The start for the Pi, an standard int.
    :param n: The integer that represent the end of the Pi.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    return csp.pi(f, i, n)


def dot(xs, ys):
    """
    The dot product of two compatible Vectors.
    :param xs: The fist vector.
    :param ys: The second vector.
    :return: The dot product.
    """
    global csp
    check_engine()
    return csp.dot(xs, ys)


def mul(xs, ys):
    """
    The elementwise product of two Vectors.
    :param xs: The fist vector.
    :param ys: The second vector.
    :return: The product.
    """
    global csp
    check_engine()
    return csp.mul(xs, ys)


def values(lst, cleaner=None):
    """
    Convert to standard values
    :param lst: List with elements.
    :param cleaner: Filter for elements.
    :return: Standard (filtered) values.
    """
    global csp
    check_engine()
    return csp.values(lst, cleaner)


def apply_single(lst, f, indexed=False):
    """
    A sequential operation over a vector.
    :param lst: The vector.
    :param f: The lambda f of one integer variable.
    :param indexed: The lambda f of two integer variable, the first is an index.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    if indexed:
        csp.apply_indexed(lst, single=f)
    else:
        csp.apply(lst, single=f)


def apply_dual(lst, f, indexed=False):
    """
    A cross operation over a vector on all pairs i, j such that i < j elements.
    :param lst: The vector.
    :param f: The lambda f of two integer variables.
    :param indexed: The lambda f of four integer variable, the 2 firsts are indexes.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    if indexed:
        csp.apply_indexed(lst, dual=f)
    else:
        csp.apply(lst, dual=f)


def apply_different(lst, f, indexed=False):
    """
    A cross operation over a vector on all pairs i, j such that i != j elements.
    :param lst: The vector.
    :param f: The lambda f of two integer variables.
    :param indexed: The lambda f of four integer variable, the 2 firsts are indexes.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    if indexed:
        csp.apply_indexed(lst, different=f)
    else:
        csp.apply(lst, different=f)


def all_different(args):
    """
    The all different global constraint.
    :param args: A vector of integers.
    :return:
    """
    global csp
    check_engine()
    csp.apply(args, dual=lambda x, y: x != y)


def all_out(args, values):
    """
    The all different to values global constraint.
    :param args: A vector of integers.
    :param values: The values excluded.
    :return:
    """
    global csp
    check_engine()
    csp.apply(args, single=lambda x: [x != v for v in values])


def all_in(args, values):
    """
    The all in values global constraint.
    :param args: A vector of integers.
    :param values: The values included.
    :return:
    """
    global csp
    check_engine()
    csp.apply(args, single=lambda x: x == one_of(values))


def flatten(mtx):
    """
    Flatten a matrix into list.
    :param mtx: The matrix.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    return csp.flatten(mtx)


def bits():
    """
    The current bits for the engine.
    :return: The bits
    """
    check_engine()
    return csp.bits


def oo():
    """
    The infinite for rhe system, the maximal value for the current engine.
    :return: 2 ** bits - 1
    """
    global csp
    check_engine()
    return csp.oo


def element(item, data):
    """
    Ensure that the element i is on the data, on the position index.
    :param item: The element
    :param data: The data
    :return: The position of element
    """
    global csp
    check_engine()
    ith = integer()
    csp.variables.append(ith)
    csp.element(ith, data, item)
    return csp.variables[-1]


def index(ith, data):
    """
    Ensure that the element i is on the data, on the position index.
    :param ith: The element
    :param data: The data
    :return: The position of element
    """
    global csp
    check_engine()
    item = integer()
    csp.variables.append(item)
    csp.element(ith, data, item)
    return csp.variables[-1]


def gaussian(x=None, y=None):
    """
    Create a gaussian integer from (x+yj).
    :param x: real
    :param y: imaginary
    :return: (x+yj)
    """
    check_engine()
    if x is None and y is None:
        return Gaussian(integer(), integer())
    return Gaussian(x, y)


def rational(x=None, y=None):
    """
    Create a rational x / y.
    :param x: numerator
    :param y: denominator
    :return: x / y
    """
    check_engine()
    if x is None and y is None:
        return Rational(integer(), integer())
    return Rational(x, y)


def at_most_k(x, k):
    """
    At most k bits can be activated for this integer.
    :param x: An integer.
    :param k: k elements
    :return: The encoded variable
    """
    global csp
    check_engine()
    return csp.at_most_k(x, k)


def sqrt(x):
    """
    Define x as a perfect square.
    :param x: The integer
    :return: The square of this integer.
    """
    global csp
    check_engine()
    return csp.sqrt(x)


# ///////////////////////////////////////////////////////////////////////////////
# //        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
# //                        oscar.riveros@peqnp.science                        //
# //                                                                           //
# //   without any restriction, Oscar Riveros reserved rights, patents and     //
# //  commercialization of this knowledge or derived directly from this work.  //
# ///////////////////////////////////////////////////////////////////////////////
def hess_sequence(n, oracle, fast=True, cycles=1):
    """
    HESS Algorithm is a Universal Black Box Optimizer (sequence version).
    :param n: The size of sequence.
    :param oracle: The oracle, this output a number and input a sequence.
    :param fast: More fast less accuracy.
    :param cycles: How many times the HESS algorithm is executed.
    :return optimized sequence.
    """
    xs = list(range(n))
    glb = oracle(xs) + 1
    opt = xs[:]

    def __inv(a, b, xs):
        i, j = min(a, b), max(a, b)
        while i < j:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1

    top = glb
    for i in range(cycles):
        glb = top + 1
        if fast:
            while True:
                anchor = glb
                for i in range(len(xs) - 1):
                    for j in range(i + 1, len(xs)):
                        __inv(i, j, xs)
                        loc = oracle(xs)
                        if loc == top:
                            glb *= 2
                        if loc < glb:
                            glb = loc
                            if glb < top:
                                top = glb
                                opt = xs[:]
                        elif loc > glb:
                            __inv(i, j, xs)
                if anchor == glb:
                    break
        else:
            while True:
                anchor = glb
                for i in range(len(xs)):
                    for j in range(len(xs)):
                        __inv(i, j, xs)
                        loc = oracle(xs)
                        if loc == top:
                            glb *= 2
                        if loc < glb:
                            glb = loc
                            if glb < top:
                                top = glb
                                opt = xs[:]
                        elif loc > glb:
                            __inv(i, j, xs)
                if anchor == glb:
                    break

    return opt


# ///////////////////////////////////////////////////////////////////////////////
# //        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
# //                        oscar.riveros@peqnp.science                        //
# //                                                                           //
# //   without any restriction, Oscar Riveros reserved rights, patents and     //
# //  commercialization of this knowledge or derived directly from this work.  //
# ///////////////////////////////////////////////////////////////////////////////
def hess_binary(n, oracle, fast=True, cycles=1):
    """
    HESS Algorithm is a Universal Black Box Optimizer (binary version).
    :param n: The size of bit vector.
    :param oracle: The oracle, this output a number and input a bit vector.
    :param fast: More fast some times less accuracy.
    :param cycles: How many times the HESS algorithm is executed.
    :return optimized sequence.
    """
    xs = [False] * n
    glb = oracle(xs) + 1
    opt = xs[:]

    def __inv(i, j, xs):
        if xs[i] == xs[j]:
            xs[j] = not xs[i]
        else:
            aux = xs[i]
            xs[i] = not xs[j]
            xs[j] = aux

    top = glb
    for i in range(cycles):
        glb = top + 1
        if fast:
            while True:
                anchor = glb
                for i in range(len(xs) - 1):
                    for j in range(i + 1, len(xs)):
                        __inv(i, j, xs)
                        loc = oracle(xs)
                        if loc == top:
                            glb *= 2
                        if loc < glb:
                            glb = loc
                            if glb < top:
                                top = glb
                                opt = xs[:]
                        elif loc > glb:
                            __inv(i, j, xs)
                if anchor == glb:
                    break
        else:
            while True:
                anchor = glb
                for i in range(len(xs)):
                    for j in range(len(xs)):
                        __inv(i, j, xs)
                        loc = oracle(xs)
                        if loc == top:
                            glb *= 2
                        if loc < glb:
                            glb = loc
                            if glb < top:
                                top = glb
                                opt = xs[:]
                        elif loc > glb:
                            __inv(i, j, xs)
                if anchor == glb:
                    break
    return opt


# ///////////////////////////////////////////////////////////////////////////////
# //        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
# //                        oscar.riveros@peqnp.science                        //
# //                                                                           //
# //   without any restriction, Oscar Riveros reserved rights, patents and     //
# //  commercialization of this knowledge or derived directly from this work.  //
# ///////////////////////////////////////////////////////////////////////////////
def hyper_loop(n, m):
    """
    An nested for loop
    :param n: The size of the samples
    :param m: The numbers in the sample 0..m
    :return:
    """
    idx = []
    for k in range(m ** n):
        for _ in range(n):
            idx.append(k % m)
            k //= m
            if len(idx) == n:
                yield idx[::-1]
                del idx[:]


def reshape(lst, dimensions):
    """
    Reshape a list
    :param lst: The coherent list to reshape
    :param dimensions:  The list of dimensions
    :return: The reshaped list
    """
    global csp
    check_engine()
    return csp.reshape(lst, dimensions)


def tensor(dimensions, key=None):
    """
    Create a tensor
    :param dimensions: The list of dimensions
    :param key: The name of tensor for CNF rendering
    :return: A tensor
    """
    global csp
    check_engine()
    csp.variables.append(csp.int(key=key, size=None, deep=dimensions))
    return csp.variables[-1]


def linear(is_real=False):
    """
    Create a linear variable.
    :param is_real: If true, the variable is a real number if not an integer.
    :return: The new variable.
    """
    global csp
    check_engine()
    csp.mips.append(Linear(csp, len(csp.mips), is_real=is_real))
    return csp.mips[-1]


def maximize(objective, solve=True, lp_path=''):
    """
    Maximize the objective, according to the current linear constrains.
    :param objective: An standard linear expression.
    :param solve: Used to render lp file solve by PIXIE if True else only render lp file.
    :param lp_path: The path for the model.
    :return: the values of the model in order of variable creation.
    """
    global csp
    ints = []
    for var in csp.mips:
        if var.is_real:
            ints.append(0)
        else:
            ints.append(1)
    csp.set_integer_condition(ints)
    opt, result = csp.maximize(objective, solve, lp_path)
    if solve:
        for v, r in zip(csp.mips, result):
            if not v.is_real:
                v.value = int(r + 0.5)
            else:
                v.value = r
        return opt
    return False


def minimize(objective, solve=True, lp_path=''):
    """
    Minimize the objective, according to the current linear constrains.
    :param objective: An standard linear expression.
    :param solve: Used to render lp file solve by PIXIE if True else only render lp file.
    :param lp_path: The path for the model.
    :return: the values of the model in order of variable creation.
    """
    global csp
    ints = []
    for var in csp.mips:
        if var.is_real:
            ints.append(0)
        else:
            ints.append(1)
    csp.set_integer_condition(ints)
    opt, result = csp.minimize(objective, solve, lp_path)
    if solve:
        for v, r in zip(csp.mips, result):
            if not v.is_real:
                v.value = int(r + 0.5)
            else:
                v.value = r
        return opt
    return None
