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

from .csp import *

csp = None
vrs = None


def check_engine():
    if csp is None:
        print('The PEQNP System is not initialized...')
        exit(0)


def version():
    """
    Print the current version of the system.
    :return:
    """
    print('c PEQNP Mathematical Solver from http://www.peqnp.com')


def begin(bits=None, key=None):
    """
    Initialize and reset the internal state of solver engine.
    :param bits: The bits 2 ** bits - 1 of solving space.
    :param file_name: file to compile the csp.
    :return:
    """
    global csp
    try:
        csp = CSP(bits, file_name=key)
    except Exception as ex:
        print('MIP and SAT solvers are not specified. \n{}'.format(ex))


def integer(bits=None):
    """
    Correspond to an integer.
    :param bits: The bits of the integer.
    :return: An instance of Integer.
    """
    global csp
    check_engine()
    csp.atoms.append(csp.int(size=bits))
    return csp.atoms[-1]


def constant(value, bits=None):
    """
    Correspond to an constant of value with bits bits.
    :param bits: The bits bits of the constant.
    :param value: The value that represent the constant.
    :return: An instance of Constant.
    """
    global csp
    check_engine()
    csp.atoms.append(csp.int(size=bits, value=value))
    return csp.atoms[-1]


def subsets(lst, k=None, complement=False):
    """
    Generate all subsets for an specific universe of data.
    :param lst: The universe of data.
    :param k: The cardinality of the subsets.
    :param complement: True if include in return the complement.
    :return: (binary representation of subsets, the generic subset representation, the complement of subset if complement=True)
    """
    global csp
    check_engine()
    bits = csp.int(size=len(lst))
    csp.atoms.append(bits)
    if k is not None:
        assert sum(constant(0).iff(-bits[i], constant(1)) for i in range(len(lst))) == k
    subset_ = [constant(0).iff(-bits[i], lst[i]) for i in range(len(lst))]
    csp.atoms += subset_
    if complement:
        complement_ = [constant(0).iff(bits[i], lst[i]) for i in range(len(lst))]
        csp.atoms += complement_
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
    csp.atoms += subset_
    if complement:
        csp.atoms += complement_
        return subset_, complement_
    return subset_


def vector(bits=None, size=None):
    """
    A vector of integers.
    :param bits: The bit bits for each integer.
    :param size: The bits of the vector.
    :return: An instance of vector.
    """
    global csp
    check_engine()
    array_ = csp.array(size=bits, dimension=size)
    csp.atoms += array_
    return array_


def matrix(bits=None, dimensions=None):
    """
    A matrix of integers.
    :param bits: The bit bits for each integer.
    :param dimensions: An tuple with the dimensions for the array (n, m).
    :return: An instance of Matrix.
    """
    global csp
    check_engine()
    matrix_ = []
    for i in range(dimensions[0]):
        row = []
        lns = []
        for j in range(dimensions[1]):
            csp.atoms.append(integer(bits=bits))
            row.append(csp.atoms[-1])
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


def permutations(lst, n):
    """
    Entangle all permutations of bits n for the vector lst.
    :param lst: The list to entangle.
    :param n: The bits of entanglement.
    :return: (indexes, values)
    """
    check_engine()
    xs = vector(size=n)
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
    return constant(0).iff(-x[ith] if neg else x[ith], constant(1))


def one_of(lst):
    """
    This indicate that at least one of the instruction on the array is active for the current problem.
    :param lst: A list of instructions.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    bits = csp.int(size=len(lst))
    assert sum(constant(0).iff(bits[i], constant(1)) for i in range(len(lst))) == 1
    return sum(constant(0).iff(bits[i], lst[i]) for i in range(len(lst)))


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


def apply_single(lst, f):
    """
    A sequential operation over a vector.
    :param lst: The vector.
    :param f: The lambda f of one integer variable.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    csp.apply(lst, single=f)


def apply_dual(lst, f):
    """
    A cross operation over a vector on all pairs i, j such that i < j elements.
    :param lst: The vector.
    :param f: The lambda f of two integer atoms.
    :return: The entangled structure.
    """
    global csp
    check_engine()
    csp.apply(lst, dual=f)


def apply_different(lst, f):
    """
    A cross operation over a vector on all pairs i, j such that i != j elements.
    :param lst: The vector.
    :param f: The lambda f of two integer atoms.
    :return: The entangled structure.
    """
    global csp
    check_engine()
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
    csp.atoms.append(ith)
    csp.element(ith, data, item)
    return csp.atoms[-1]


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
    csp.atoms.append(item)
    csp.element(ith, data, item)
    return csp.atoms[-1]


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


def tensor(dimensions):
    """
    Create a tensor
    :param dimensions: The list of dimensions
    :return: A tensor
    """
    global csp
    check_engine()
    csp.atoms.append(csp.int(size=None, deep=dimensions))
    return csp.atoms[-1]


def end(args):
    global csp, vrs
    check_engine()
    vrs = args
    csp.line_pre_adder('p cnf {} {}'.format(csp.number_of_variables, csp.number_of_clauses))
    for k, v in reversed(list(args.items())):
        csp.line_pre_adder('c {} : {}'.format(k, v.block))


def satisfy(solver, params=''):
    global csp, vrs
    import subprocess
    check_engine()
    subprocess.call('{0} {2} {1}.cnf > {1}.mod'.format(solver, csp.file_name, params), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open('{}.mod'.format(csp.file_name), 'r') as mod:
        lines = ''
        for line in mod.readlines():
            if line.startswith('v '):
                lines += line.strip('v ').strip('\n') + ' '
        if len(lines) > 0:
            model = list(map(int, lines.strip(' ').split(' ')))
            for k, v in vrs.items():
                v.value = int(''.join(map(str, [int(int(model[abs(bit) - 1]) > 0) for bit in v.block[::-1]])), 2)
            with open('{}.cnf'.format(csp.file_name), 'a') as file:
                file.write(' '.join([str(-int(literal)) for literal in model]) + '\n')
            return True
        else:
            return False
