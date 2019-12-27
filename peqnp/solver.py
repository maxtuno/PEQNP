"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""

import functools
import operator
import sys
import uuid

import slime

from peqnp.entity import Entity

sys.setrecursionlimit(1 << 16)


class CSP:
    def __init__(self, bits=None, deepness=None):
        slime.reset()
        self._map = {}
        self._bits = bits
        self._oo = 2 ** bits - 1
        self._deepness = deepness if deepness is not None else bits // 2
        self._number_of_clauses = 0
        self._ready = False
        self._number_of_variables = 0
        self._number_of_clauses = 0
        self._offset = None
        self._unitary = [-1]
        self.__0 = None
        self.__1 = None
        self._true = self.add_variable()
        self._false = -self._true
        self._unsat = True
        self._constants = {}
        self._hard = (1 << 32) - 1
        self._weight = self._hard
        self._solutions = []
        self.add_block([-self._true])

    @property
    def true(self):
        return self._true

    @property
    def false(self):
        return self._false

    @property
    def zero(self):
        if self.__0 is None:
            self.__0 = self.int()
            assert self.__0 == 0
        return self.__0

    @property
    def one(self):
        if self.__1 is None:
            self.__1 = self.int()
            assert self.__1 == 1
        return self.__1

    @property
    def oo(self):
        return self._oo

    def add_variable(self, ):
        self._number_of_variables += 1
        return self._number_of_variables

    def add_block(self, clause):
        slime.add_clause(sorted(set(clause), key=abs))
        return clause

    def mapping(self, key, value):
        self._map[key] = value
        return {key: value}

    def constraint(self, args):
        pass

    def create_block(self, size=None):
        if size:
            return [self.add_variable() for _ in range(size)]
        return [self.add_variable() for _ in range(self._bits)]

    def create_variable(self, key=None, size=None):
        if key is None:
            key = '_' + str(uuid.uuid4()).replace('-', '')
        block = self.create_block(size)
        self.add_block([-variable for variable in block])
        self.mapping(key, block)
        return key, block

    def create_constant(self, value):
        def __encode(n):
            if n in self._constants.keys():
                return self._constants[n]
            self._constants[n] = self.create_block()
            block = self._constants[n]
            for i in range(self._bits):
                if n % 2 == 0:
                    self.add_block([-block[i]])
                else:
                    self.add_block([block[i]])
                n //= 2
            self.mapping(str(value), block)
            return block

        return __encode(value)

    def or_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()

        fc = list(il)
        fc.append(-ol)
        self.add_block(fc)

        for lit in il:
            self.add_block([-lit, ol])

        return ol

    def and_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()

        fc = list(map(lambda x: -x, il))
        fc.append(ol)
        self.add_block(fc)

        for lit in il:
            self.add_block([lit, -ol])

        return ol

    def binary_xor_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()
        l1, l2 = il[0], il[1]

        self.add_block([l1, l2, -ol])
        self.add_block([-l1, -l2, -ol])
        self.add_block([l1, -l2, ol])
        self.add_block([-l1, l2, ol])

        return ol

    def binary_mux_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()
        sel, lhs, rhs = il[0], il[1], il[2]

        self.add_block([sel, lhs, -ol])
        self.add_block([sel, -lhs, ol])
        self.add_block([-sel, rhs, -ol])
        self.add_block([-sel, -rhs, ol])

        return ol

    def fas_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()

        lhs, rhs, c_in = il

        for x in [[lhs, rhs, c_in, -ol],
                  [lhs, -rhs, -c_in, -ol],
                  [lhs, -rhs, c_in, ol],
                  [lhs, rhs, -c_in, ol],
                  [-lhs, rhs, c_in, ol],
                  [-lhs, -rhs, -c_in, ol],
                  [-lhs, -rhs, c_in, -ol],
                  [-lhs, rhs, -c_in, -ol]]:
            self.add_block(x)

        return ol

    def fac_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()

        lhs, rhs, c_in = il

        for x in [[lhs, rhs, -ol],
                  [lhs, c_in, -ol],
                  [lhs, -rhs, -c_in, ol],
                  [-lhs, rhs, c_in, -ol],
                  [-lhs, -rhs, ol],
                  [-lhs, -c_in, ol]]:
            self.add_block(x)

        return ol

    def gate_vector(self, bge, lhs_il, rhs_il, ol=None):
        if ol is None:
            ol = [None] * len(lhs_il)

        return [bge((lhs, rhs), ol) for lhs, rhs, ol in zip(lhs_il, rhs_il, ol)]

    def bv_and_gate(self, lhs_il, rhs_il, ol=None):
        ol = self.gate_vector(self.and_gate, lhs_il, rhs_il, ol)
        return ol

    def bv_or_gate(self, lhs_il, rhs_il, ol=None):
        return self.gate_vector(self.or_gate, lhs_il, rhs_il, ol)

    def bv_xor_gate(self, lhs_il, rhs_il, ol=None):
        return self.gate_vector(self.binary_xor_gate, lhs_il, rhs_il, ol)

    def bv_rca_gate(self, lhs_il, rhs_il, carry_in_lit=None, ol=None, carry_out_lit=None):
        wt = min(len(lhs_il), len(rhs_il))

        if wt == 0:
            return []

        if ol is None:
            ol = [self.add_variable() for _ in range(0, wt)]

        ol = [o if o is not None else self.add_variable() for o in ol]

        crr = [self.add_variable() for _ in range(0, wt - 1)]
        crr.append(carry_out_lit)

        if carry_in_lit is not None:
            adi = (lhs_il[0], rhs_il[0], carry_in_lit)
            self.fas_gate(adi, ol[0])
            if crr[0] is not None:
                self.fac_gate(adi, crr[0])
        else:
            adi = (lhs_il[0], rhs_il[0])
            self.binary_xor_gate(adi, ol[0])
            if crr[0] is not None:
                self.and_gate(adi, crr[0])

        for i in range(1, wt):
            adi = (lhs_il[i], rhs_il[i], crr[i - 1])
            self.fas_gate(adi, ol[i])
            if crr[i] is not None:
                self.fac_gate(adi, crr[i])

        return ol

    def bv_rcs_gate(self, lhs_il, rhs_il, ol=None):
        fl_rhs = [-x for x in rhs_il]
        one = self.add_variable()
        self.add_block([one])
        return self.bv_rca_gate(lhs_il=lhs_il, rhs_il=fl_rhs, carry_in_lit=one, ol=ol)

    def bv_pm_gate(self, lhs_il, rhs_il, ol=None, ow_lit=None):
        wt = len(lhs_il)

        if wt == 0:
            return []

        def __cfl(n):
            return [self.add_variable() for _ in range(0, n)]

        if ol is None:
            ol = __cfl(wt)
        else:
            ol = list(map(lambda l: self.add_variable() if l is None else l, ol))

        pp = [[ol[0]] + __cfl(wt - 1)]
        l_lhs = lhs_il[0]
        self.bv_and_gate(rhs_il, [l_lhs] * wt, pp[0])
        if ow_lit is not None:
            pp += [self.bv_and_gate(rhs_il, [l] * wt) for l in lhs_il[1:]]
        else:
            pp += [self.bv_and_gate(rhs_il[0:wt - i], [lhs_il[i]] * (wt - i)) for i in range(1, wt)]
        partial_sums = [([ol[i]] + __cfl(wt - i - 1)) for i in range(1, wt)]
        csc = __cfl(wt - 1) if ow_lit is not None else [None] * (wt - 1)

        cps = pp[0][1:wt]
        for i in range(1, wt):
            cpp = pp[i][0:wt - i]
            psa = partial_sums[i - 1]
            assert len(cps) == wt - i
            self.bv_rca_gate(lhs_il=cps, rhs_il=cpp, ol=psa, carry_out_lit=csc[i - 1])
            cps = psa[1:]

        if ow_lit is not None:
            ow = csc[:]
            for i in range(1, wt):
                ow += pp[i][wt - i:wt]
            self.or_gate(ow, ow_lit)

        return ol

    def bv_ule_gate(self, lhs_il, rhs_il, ol=None):
        if ol is None:
            ol = self.add_variable()

        if len(lhs_il) == 0:
            self.add_block([ol])
            return ol

        if len(lhs_il) == 1:
            self.and_gate([lhs_il[0], -rhs_il[0]], -ol)
            return ol

        wt = len(lhs_il)
        rl = self.bv_ule_gate(lhs_il[:wt - 1], rhs_il[:wt - 1])

        lhs_msb, rhs_msb = lhs_il[wt - 1], rhs_il[wt - 1]
        msb_is_lt = self.and_gate([-lhs_msb, rhs_msb])
        msb_is_eq = -self.binary_xor_gate([lhs_msb, rhs_msb])

        leq_if_first_is_eq = self.and_gate([msb_is_eq, rl])
        return self.or_gate([msb_is_lt, leq_if_first_is_eq], ol)

    def bv_sle_gate(self, lhs_il, rhs_il, ol=None):

        if ol is None:
            ol = self.add_variable()

        if len(lhs_il) == 0:
            self.add_block([ol])
            return ol

        if len(lhs_il) == 1:
            return self.or_gate([lhs_il[0], -rhs_il[0]], ol)

        wt = len(lhs_il)
        lhs_msb = lhs_il[wt - 1]
        rhs_msb = rhs_il[wt - 1]
        rest_leq = self.bv_ule_gate(lhs_il=lhs_il[:wt - 1], rhs_il=rhs_il[:wt - 1])
        msb_eq = -self.binary_xor_gate(il=[lhs_msb, rhs_msb])
        sleq = self.and_gate(il=[msb_eq, rest_leq])
        npos = self.and_gate(il=[lhs_msb, -rhs_msb])
        return self.or_gate(il=[npos, sleq], ol=ol)

    def bv_eq_gate(self, lhs_il, rhs_il, ol=None):

        if ol is None:
            ol = self.add_variable()

        dif = self.bv_xor_gate(lhs_il, rhs_il)
        self.or_gate(dif, -ol)
        return ol

    def bv_mux_gate(self, lhs_il, rhs_il, s_lhs_lit=None, ol=None):
        s_lhs_lit = self.add_variable() if s_lhs_lit is None else s_lhs_lit
        lhs_s = self.bv_and_gate(lhs_il=lhs_il, rhs_il=[s_lhs_lit] * len(lhs_il))
        rhs_s = self.bv_and_gate(lhs_il=rhs_il, rhs_il=[-s_lhs_lit] * len(rhs_il))
        return self.bv_or_gate(lhs_il=lhs_s, rhs_il=rhs_s, ol=ol)

    def bv_lud_gate(self, lhs_il, rhs_il, ol=None, remainder_ol=None):
        wt = len(lhs_il)

        if wt == 0:
            return []

        def __cfl(n):
            return [self.add_variable() for _ in range(0, n)]

        cf = self.add_variable()
        self.add_block([-cf])

        dnz = self.stg_or_gate(il=rhs_il)

        qt = __cfl(wt)

        rem = list()
        for step_idx in reversed(range(0, wt)):
            rem = [lhs_il[step_idx]] + rem

            if len(rem) == len(rhs_il):
                self.bv_ule_gate(lhs_il=rhs_il, rhs_il=rem, ol=qt[step_idx])
            else:
                lbc = self.bv_ule_gate(lhs_il=rhs_il[0:len(rem)], rhs_il=rem)
                hbc = dnz[len(rem)]
                self.and_gate(il=[lbc, -hbc], ol=qt[step_idx])

            rmd = self.bv_rcs_gate(lhs_il=rem, rhs_il=rhs_il[0:len(rem)])

            rem = self.bv_mux_gate(lhs_il=rmd, rhs_il=rem, s_lhs_lit=qt[step_idx])

        rhs_is_zero = -self.or_gate(il=rhs_il)

        if remainder_ol is not None:
            self.bv_and_gate(lhs_il=[-rhs_is_zero] * wt, rhs_il=rem, ol=remainder_ol)

        return self.bv_and_gate(lhs_il=[-rhs_is_zero] * wt, rhs_il=qt, ol=ol)

    def bv_lur_gate(self, lhs_il, rhs_il, ol=None):
        if ol is None:
            ol = [self.add_variable() for _ in lhs_il]
        else:
            ol = [self.add_variable() if x is None else x for x in ol]

        self.bv_lud_gate(
            lhs_il=lhs_il, rhs_il=rhs_il,
            remainder_ol=ol)

        return ol

    def stg_or_gate(self, il, ol=None):
        wt = len(il)

        if wt == 0:
            return []

        if ol is None:
            result = [self.add_variable() for _ in range(0, wt)]
        else:
            result = [out_lit if out_lit is not None else self.add_variable() for out_lit in ol]

        self.or_gate(il=[il[-1]], ol=result[-1])

        for idx in reversed(range(0, wt - 1)):
            self.or_gate(il=[il[idx], result[idx + 1]], ol=result[idx])

        return result

    @property
    def bits(self):
        return self._bits

    @property
    def deepness(self):
        return self._deepness

    @deepness.setter
    def deepness(self, value):
        self._deepness = value

    @property
    def unsat(self):
        return self._unsat

    @property
    def hard(self):
        return self._hard

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = str(weight)

    def to_sat(self, args, solve=False, turbo=False):
        if solve:
            model = slime.solve(turbo)
            if model:
                for key, value in self._map.items():
                    for arg in args:
                        if isinstance(arg, Entity) and arg.key == key:
                            arg._value = self.normalize(int(''.join(map(str, [int(int(model[abs(bit) - 1]) > 0) for bit in value[::-1]])), 2))
                self.add_block([-lit for lit in model])
                self._unsat = False
                return True
            else:
                self._unsat = False
        return False

    def int(self, key=None, block=None, value=None, size=None):
        return Entity(self, key=key, block=block, value=value, size=size)

    def array(self, dimension, size=None, key=None):
        if size is not None:
            if key is not None:
                return [self.int(key='{}_{}'.format(key, i), size=size) for i in range(dimension)]
            return [self.int(size=size) for _ in range(dimension)]
        if key is not None:
            return [self.int(key='{}_{}'.format(key, i)) for i in range(dimension)]
        return [self.int() for _ in range(dimension)]

    def element(self, x, lst, y):
        idx = self.int(size=len(lst))
        self.at_most_k(idx, 1)
        for i in range(len(lst)):
            assert self.zero.iff(idx[i], i) == self.zero.iff(idx[i], x)
            assert self.zero.iff(idx[i], lst[i]) == self.zero.iff(idx[i], y)

    def indexing(self, xs, ys, lst):
        n = len(xs)
        for i in range(n):
            self.element(n * xs[i] + xs[(i + 1) % n], lst, ys[i])

    def asymmetrical_indexing(self, xs, ys, lst):
        n = len(xs)
        m = len(ys)
        zs = self.array(m)
        for i in range(m):
            self.element(zs[i], lst, ys[i])
            assert xs[i % n] * n + xs[(i + 1) % n] == zs[i]

    def sequencing(self, xs, ys, lst):
        n = len(xs)
        zs = self.array(n)
        for i in range(n):
            self.element(zs[i], lst, ys[i])
            assert xs[i] == zs[i]

    def permutations(self, xs, lst):
        n = len(xs)
        zs = self.array(n)
        for i in range(n):
            self.element(zs[i], lst, xs[i])
        self.apply(zs, single=lambda a: a < n)
        self.apply(zs, dual=lambda a, b: a != b)

    def combinations(self, xs, lst):
        n = len(xs)
        zs = self.array(n)
        for i in range(n):
            self.element(zs[i], lst, xs[i])

    def factorial(self, x):
        aa = Entity(self, size=self.bits)
        assert sum([self.zero.iff(aa[i], self.one) for i in range(self.bits)]) == self.one
        assert sum([self.zero.iff(aa[i], i) for i in range(self.bits)]) == x
        return sum([self.zero.iff(aa[i], functools.reduce(operator.mul, [x - j for j in range(i)])) for i in range(1, self.bits)])

    def sigma(self, f, i, n):
        def __sum(xs):
            if xs:
                return functools.reduce(operator.add, xs)
            return self.zero

        aa = Entity(self, size=self.bits)
        assert sum([self.zero.iff(aa[j], self.one) for j in range(self.bits)]) == self.one
        assert sum([self.zero.iff(aa[j], j) for j in range(self.bits)]) == n + self.one
        return sum([self.zero.iff(aa[j], __sum([f(j) for j in range(i, j)])) for j in range(i, self.bits)])

    def pi(self, f, i, n):
        def __pi(xs):
            if xs:
                return functools.reduce(operator.mul, xs)
            return self.one

        aa = Entity(self, size=self.bits)
        assert sum([self.zero.iff(aa[j], self.one) for j in range(self.bits)]) == self.one
        assert sum([self.zero.iff(aa[j], j) for j in range(self.bits)]) == n + self.one
        return sum([self.zero.iff(aa[j], __pi([f(j) for j in range(i, j)])) for j in range(i, self.bits)])

    def sqrt(self, x):
        y = self.int()
        assert x == y ** 2
        return y

    def at_most_k(self, x, k):
        k += 1
        self.add_block([-lit for lit in x._block])
        import itertools
        for sub in itertools.combinations(x._block, k):
            self.add_block(sub)
        return x

    def subset(self, k, data, empty=None):
        x = self.int(size=len(data))
        self.at_most_k(x, k)
        y = self.array(len(data))
        for i in range(len(data)):
            assert self.zero.iff(x[i], data[i]) == self.zero.iff(x[i], y[i])
            assert self.zero.iff(-x[i], self.zero if empty is None else empty) == self.zero.iff(-x[i], y[i])
        return y

    @staticmethod
    def mul(xs, ys):
        return [x * y for x, y in zip(xs, ys)]

    @staticmethod
    def dot(xs, ys):
        return sum([x * y for x, y in zip(xs, ys)])

    @staticmethod
    def values(xs, cleaner=None):
        if cleaner is not None:
            return list(filter(cleaner, [x.value for x in xs]))
        return [x.value for x in xs]

    @staticmethod
    def flatten(xs):
        return [item for sublist in xs for item in sublist]

    @staticmethod
    def apply(xs, single=None, dual=None):
        for i in range(len(xs)):
            if single is not None:
                single(xs[i])
            if dual is not None:
                for j in range(i + 1, len(xs)):
                    dual(xs[i], xs[j])

    @staticmethod
    def apply_indexed(xs, single=None, dual=None):
        for i in range(len(xs)):
            if single is not None:
                single(i, xs[i])
            if dual is not None:
                for j in range(i + 1, len(xs)):
                    dual(i, j, xs[i], xs[j])

    def normalize(self, value):
        return value

    def negative(self, value):
        return value - (1 << self._bits)


def hess_sequence(n, oracle):
    xs = list(range(n))
    glb = oracle(xs)
    opt = xs[:]

    def __inv(a, b, xs):
        i, j = min(a, b), max(a, b)
        while i < j:
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
            j -= 1

    while True:
        anchor = glb
        for i in range(len(xs)):
            for j in range(len(xs)):
                __inv(i, j, xs)
                loc = oracle(xs)
                if loc < glb:
                    glb = loc
                    opt = xs[:]
                elif loc > glb:
                    __inv(i, j, xs)
        if anchor == glb:
            break
    return opt


def hess_binary(n, oracle):
    xs = [False] * n
    glb = oracle(xs)
    opt = xs[:]

    def __inv(i, j, xs):
        if xs[i] == xs[j]:
            xs[i] = not xs[j]
        else:
            aux = xs[i]
            xs[i] = not xs[j]
            xs[j] = aux

    while True:
        anchor = glb
        for i in range(len(xs)):
            for j in range(len(xs)):
                __inv(i, j, xs)
                loc = oracle(xs)
                if loc < glb:
                    glb = loc
                    opt = xs[:]
                elif loc > glb:
                    __inv(i, j, xs)
        if anchor == glb:
            break
    return opt
