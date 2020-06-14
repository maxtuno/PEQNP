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

from .atom import Atom


class CSP:
    def __init__(self, bits, file_name):
        import sys
        sys.setrecursionlimit(1 << 16)
        self.file_name = file_name
        self.file = open(self.file_name + '.cnf', 'w')
        self.atoms = []
        self.map = {}
        self.bits = bits
        self.oo = 2 ** bits - 1
        self.number_of_clauses = 0
        self.number_of_variables = 0
        self.true = self.add_variable()
        self.false = -self.true
        self.constants = {}
        self.add_block([-self.true])

    def line_pre_adder(self, content):
        import fileinput
        self.file.close()
        f = fileinput.input(self.file_name + '.cnf', inplace=1)
        for line in f:
            if f.isfirstline():
                print(content.rstrip('\r\n') + '\n' + line.rstrip('\r\n'))
            else:
                print(line.rstrip('\r\n'))

    def add_variable(self):
        self.number_of_variables += 1
        return self.number_of_variables

    def add_block(self, clause):
        self.number_of_clauses += 1
        for lit in clause:
            self.file.write('{} '.format(lit))
        self.file.write('0\n')
        return clause

    def create_block(self, size=None):
        if size:
            return [self.add_variable() for _ in range(size)]
        return [self.add_variable() for _ in range(self.bits)]

    def create_variable(self, size=None):
        block = self.create_block(size)
        self.add_block([-variable for variable in block])
        return block

    def constant(self, value):
        def __encode(n):
            if n in self.constants.keys():
                return self.constants[n]
            self.constants[n] = self.create_block()
            block = self.constants[n]
            n = abs(n)
            for i in range(self.bits):
                if (n % 2 == 0) == (value >= 0):
                    self.add_block([-block[i]])
                else:
                    self.add_block([block[i]])
                n //= 2
            return block

        return __encode(value)

    def or_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()
        self.add_block(il + [-ol])
        for lit in il:
            self.add_block([-lit, ol])
        return ol

    def and_gate(self, il, ol=None):
        if ol is None:
            ol = self.add_variable()
        self.add_block([-lit for lit in il] + [ol])
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

    @staticmethod
    def gate_vector(bge, lhs_il, rhs_il, ol=None):
        if ol is None:
            ol = [None] * len(lhs_il)
        return [bge([lhs, rhs], ol) for lhs, rhs, ol in zip(lhs_il, rhs_il, ol)]

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

    def int(self, block=None, value=None, size=None, deep=None):
        return Atom(self, block=block, value=value, bits=size, deep=deep)

    def array(self, dimension, size=None):
        if size is not None:
            return [self.int(size=size) for _ in range(dimension)]
        return [self.int() for _ in range(dimension)]

    def element(self, x, lst, y):
        idx = self.int(size=len(lst))
        self.at_most_k(idx, 1)
        for i in range(len(lst)):
            assert self.int(value=0).iff(idx[i], i) == self.int(value=0).iff(idx[i], x)
            assert self.int(value=0).iff(idx[i], lst[i]) == self.int(value=0).iff(idx[i], y)

    def indexing(self, xs, ys, lst):
        n = len(xs)
        for i in range(n):
            self.element(n * xs[i] + xs[(i + 1) % n], lst, ys[i])

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
        import functools
        import operator
        sub = Atom(self, bits=self.bits)
        assert sum([self.int(value=0).iff(sub[i], self.int(value=1)) for i in range(self.bits)]) == self.int(value=1)
        assert sum([self.int(value=0).iff(sub[i], i) for i in range(self.bits)]) == x
        return sum([self.int(value=0).iff(sub[i], functools.reduce(operator.mul, [x - j for j in range(i)])) for i in range(1, self.bits)])

    def sigma(self, f, i, n):
        import functools
        import operator

        def __sum(xs):
            if xs:
                return functools.reduce(operator.add, xs)
            return self.int(value=0)

        sub = Atom(self, bits=self.bits)
        assert sum([self.int(value=0).iff(sub[j], self.int(value=1)) for j in range(self.bits)]) == self.int(value=1)
        assert sum([self.int(value=0).iff(sub[j], j) for j in range(self.bits)]) == n + self.int(value=1)
        return sum([self.int(value=0).iff(sub[j], __sum([f(j) for j in range(i, j)])) for j in range(i, self.bits)])

    def pi(self, f, i, n):
        import functools
        import operator

        def __pi(xs):
            if xs:
                return functools.reduce(operator.mul, xs)
            return self.int(value=1)

        sub = Atom(self, bits=self.bits)
        assert sum([self.int(value=0).iff(sub[j], self.int(value=1)) for j in range(self.bits)]) == self.int(value=1)
        assert sum([self.int(value=0).iff(sub[j], j) for j in range(self.bits)]) == n + self.int(value=1)
        return sum([self.int(value=0).iff(sub[j], __pi([f(j) for j in range(i, j)])) for j in range(i, self.bits)])

    def sqrt(self, x):
        y = self.int()
        assert x == y ** 2
        return y

    def at_most_k(self, x, k):
        k += 1
        self.add_block([-lit for lit in x.block])
        import itertools
        for sub in itertools.combinations(x.block, k):
            self.add_block(sub)
        return x

    def subset(self, k, data, empty=None, complement=False):
        x = self.int(size=len(data))
        self.at_most_k(x, k)
        y = self.array(len(data))
        if complement:
            z = self.array(len(data))
        for i in range(len(data)):
            assert self.int(value=0).iff(x[i], data[i]) == self.int(value=0).iff(x[i], y[i])
            if complement:
                assert self.int(value=0).iff(-x[i], data[i]) == self.int(value=0).iff(-x[i], z[i])
            assert self.int(value=0).iff(-x[i], self.int(value=0) if empty is None else empty) == self.int(value=0).iff(-x[i], y[i])
        if complement:
            return y, z
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
    def apply(xs, single=None, dual=None, different=None):
        for i in range(len(xs)):
            if single is not None:
                single(xs[i])
            if dual is not None:
                for j in range(i + 1, len(xs)):
                    dual(xs[i], xs[j])
            if different is not None:
                for j in range(len(xs)):
                    if i != j:
                        different(xs[i], xs[j])

    @staticmethod
    def apply_indexed(xs, single=None, dual=None):
        for i in range(len(xs)):
            if single is not None:
                single(i, xs[i])
            if dual is not None:
                for j in range(i + 1, len(xs)):
                    dual(i, j, xs[i], xs[j])

    def reshape(self, lst, shape):
        from functools import reduce
        from operator import mul
        if len(shape) == 1:
            return lst
        n = reduce(mul, shape[1:])
        return [self.reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]
