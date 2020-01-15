# The standard high level library

```python
    def version():
        """
        Print the current version of the system.
        :return:
        """
    
    def engine(bits=None, deepness=None):
        """
        Initialize and reset the internal state of solver engine.
        :param bits: The size \(2^{bits} - 1\) of solving space.
        :param deepness: The scope for the exponential variables \(bits / 4\) by default.
        :return:
        """
    
    def slime4(cnf_path, model_path='', proof_path=''):
        """
        Use directly the SLIME 4 SAT Solver.
        :param cnf_path: The cnf file to solve.
        :param model_path: The path to the model if SAT, optional.
        :param proof_path: The path for the DRUP-PROOF if UNSAT, optional.
        :return: A List with the model if SAT else an empty list.
        """
    
    def integer(key=None, bits=None):
        """
        Correspond to an integer of name key, and size bits.
        :param key: The name of variable, appear on CNF when cnf_path is setting on satisfy().
        :param bits: The bits size of the integer.
        :return: An instance of Integer.
        """
    
    def constant(value=None, bits=None):
        """
        Correspond to an constant of value with size bits.
        :param bits: The bits size of the constant.
        :param value: The value that represent the constant.
        :return: An instance of Constant.
        """
    
    def satisfy(solve=True, turbo=False, log=False, assumptions=None, cnf_path='', model_path='', proof_path='', normalize=False):
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
    
    def subsets(lst, k=None, key=None):
        """
        Generate all subsets for an specific universe of data.
        :param lst: The universe of data.
        :param k: The cardinality of the subsets.
        :param key: The name os the binary representation of subsets.
        :return: (binary representation of subsets, the generic subset representation)
        """
    
    def subset(data, k, empty=None):
        """
        An operative structure (like integer ot constant) that represent a subset of at most k elements.
        :param data: The data for the subsets.
        :param k: The maximal size for subsets.
        :param empty: The empty element, 0, by default.
        :return: An instance of Subset.
        """
    
    def vector(key=None, bits=None, size=None):
        """
        A vector of integers.
        :param key: The generic name for the array this appear indexed on cnf.
        :param bits: The bit size for each integer.
        :param size: The size of the vector.
        :return: An instance of vector.
        """
    
    def matrix(key=None, bits=None, dimensions=None):
        """
        A matrix of integers.
        :param key: The generic name for the array this appear indexed on cnf.
        :param bits: The bit size for each integer.
        :param dimensions: An tuple with the dimensions for the array (n, m).
        :return: An instance of Matrix.
        """
    
    def matrix_permutation(lst, n):
        """
        This generate the permutations for an square matrix.
        :param lst: The flattened matrix of data, i.e. a vector.
        :param n: The dimension for the square nxn-matrix.
        :return: An tuple with (index for the elements, the elements that represent the indexes)
        """
    
    def permutations(lst, n):
        """
        Entangle all permutations of size n for the vector lst.
        :param lst: The list to entangle.
        :param n: The size of entanglement.
        :return: (indexes, values)
        """
    
    def combinations(lst, n):
        """
        Entangle all combinations of size n for the vector lst.
        :param lst: The list to entangle.
        :param n: The size of entanglement.
        :return: (indexes, values)
        """
    
    def all_binaries(lst):
        """
        This say that, the vector of integer are all binaries.
        :param lst: The vector of integers.
        :return:
        """
    
    def switch(x, ith, neg=False):
        """
        This conditionally flip the internal bit for an integer.
        :param x: The integer.
        :param ith: Indicate the ith bit.
        :param neg: indicate if the condition is inverted.
        :return: 0 if the uth bit for the argument collapse to true else return 1, if neg is active exchange 1 by 0.
        """
    
    def one_of(lst):
        """
        This indicate that at least one of the instruction on the array is active for the current problem.
        :param lst: A list of instructions.
        :return: The entangled structure.
        """
    
    def factorial(x):
        """
        The factorial for the integer.
        :param x: The integer.
        :return: The factorial.
        """
    
    def sigma(f, i, n):
        """
        The Sum for i to n, for the lambda f f,
        :param f: A lambda f with an standard int parameter.
        :param i: The start for the Sum, an standard int.
        :param n: The integer that represent the end of the Sum.
        :return: The entangled structure.
        """
    
    def pi(f, i, n):
        """
        The Pi for i to n, for the lambda f f,
        :param f: A lambda f with an standard int parameter.
        :param i: The start for the Pi, an standard int.
        :param n: The integer that represent the end of the Pi.
        :return: The entangled structure.
        """
    
    def dot(xs, ys):
        """
        The dot product of two compatible Vectors.
        :param xs: The fist vector.
        :param ys: The second vector.
        :return: The dot product.
        """
    
    def mul(xs, ys):
        """
        The elementwise product of two Vectors.
        :param xs: The fist vector.
        :param ys: The second vector.
        :return: The product.
        """
    
    def apply_single(lst, f):
        """
        A sequential operation over a vector.
        :param lst: The vector.
        :param f: The lambda f of one integer variable.
        :return: The entangled structure.
        """
    
    def apply_dual(lst, f):
        """
        A cross operation over a vector.
        :param lst: The vector.
        :param f: The lambda f of two integer variables.
        :return: The entangled structure.
        """
    
    def all_different(args):
        """
        The all different global constraint.
        :param args: A vector of integers.
        :return:
        """
    
    def flatten(mtx):
        """
        Flatten a matrix into list.
        :param mtx: The matrix.
        :return: The entangled structure.
        """
    
    def bits():
        """
        The current bits for the engine.
        :return: The bits
        """
    
    def oo():
        """
        The infinite for rhe system, the maximal value for the current engine.
        :return: 2 ** bits - 1
        """
    
    def element(item, data):
        """
        Ensure that the element i is on the data, on the position index.
        :param item: The element
        :param data: The data
        :return: The position of element
        """
    
    def index(ith, data):
        """
        Ensure that the element i is on the data, on the position index.
        :param ith: The element
        :param data: The data
        :return: The position of element
        """
    
    def gaussian(x, y):
        """
        Create a gaussian integer from (x+yj).
        :param x: real
        :param y: imaginary
        :return: (x+yj)
        """
    
    def rational(x, y):
        """
        Create a rational x / y.
        :param x: numerator
        :param y: denominator
        :return: x / y
        """
    
    def at_most_k(x, k):
        """
        At most k bits can be activated for this integer.
        :param x: An integer.
        :param k: k elements
        :return: The encoded variable
        """
    
    def sqrt(x):
        """
        Define x as a perfect square.
        :param x: The integer
        :return: The square of this integer.
        """
```