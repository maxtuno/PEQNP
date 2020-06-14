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


class Atom:
    def __init__(self, encoder, block=None, value=None, bits=None, deep=None):
        self.model = []
        self.block = block
        self.encoder = encoder
        self.value = None
        self.data = []
        self.bits = bits
        self.deep = deep
        self.bin = []
        if bits is None:
            self.bits = self.encoder.bits
            self.deep = [self.bits]
        if deep is not None:
            import functools
            import operator
            self.deep = [deep] if isinstance(deep, int) else deep
            self.bits = functools.reduce(operator.mul, self.deep)
            self.block = self.encoder.create_variable(self.bits)
            self.data = self.encoder.reshape(self.block, self.deep)
        elif block is None and bits is None and value is None:
            self.block = self.encoder.create_variable()
        elif block is None and bits is not None and value is None:
            self.block = self.encoder.create_variable(self.bits)
        elif value is not None:
            self.block = self.encoder.constant(value)
        else:
            self.block = block
        if not self.data:
            self.data = self.block
        if not self.deep:
            self.deep = [self.bits]

    def is_in(self, item):
        bits = self.encoder.int(size=len(item))
        assert sum(self.encoder.int(value=0).iff(bits[i], self.encoder.int(value=1)) for i in range(len(item))) == 1
        assert sum(self.encoder.int(value=0).iff(bits[i], item[i]) for i in range(len(item))) == self
        return self

    def is_not_in(self, item):
        for element in item:
            assert self != element
        return self

    def __add__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value + other.value
            return self.value + other
        output_block = self.encoder.create_block()
        if isinstance(other, Atom):
            self.encoder.bv_rca_gate(self.block, other.block, self.encoder.true, output_block, self.encoder.true)
        else:
            self.encoder.bv_rca_gate(self.block, self.encoder.constant(other), self.encoder.true, output_block, self.encoder.true)
        return Atom(self.encoder, block=output_block)

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value == other.value
            else:
                return self.value == other
        if isinstance(other, Atom):
            return self.encoder.bv_eq_gate(self.block, other.block, self.encoder.false)
        return self.encoder.bv_eq_gate(self.block, self.encoder.constant(other), self.encoder.false)

    def __mod__(self, other):
        assert other != 0
        if self.value is not None and other.value is not None:
            return self.value % other.value
        if self.value is not None and other.value is None:
            return self.value % other
        output_block = self.encoder.create_block()
        if isinstance(other, Atom):
            self.encoder.bv_lur_gate(self.block, other.block, output_block)
        else:
            self.encoder.bv_lur_gate(self.block, self.encoder.constant(other), output_block)
        return Atom(self.encoder, block=output_block)

    def __ne__(self, other):
        if isinstance(other, Atom):
            return self.encoder.bv_eq_gate(self.block, other.block, self.encoder.true)
        return self.encoder.bv_eq_gate(self.block, self.encoder.constant(other), self.encoder.true)

    def __mul__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value * other.value
            return self.value * other
        output_block = self.encoder.create_block()
        if isinstance(other, Atom):
            self.encoder.bv_pm_gate(self.block, other.block, output_block, self.encoder.true)
        else:
            self.encoder.bv_pm_gate(self.block, self.encoder.constant(other), output_block, self.encoder.true)
        return Atom(self.encoder, block=output_block)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        if self.value is not None and not isinstance(power, Atom):
            return self.value ** power
        elif self.value is not None and power.value is not None:
            if modulo is not None:
                return pow(self.value, power.value, modulo)
            return self.value ** power.value
        else:
            if isinstance(power, Atom):
                aa = Atom(self.encoder, bits=self.bits.bit_length())
                assert sum([self.encoder.int(value=0).iff(aa[i], self.encoder.true) for i in range(self.bits.bit_length())]) == 1
                assert sum([self.encoder.int(value=0).iff(aa[i], i) for i in range(self.bits.bit_length())]) == power
                if modulo is not None:
                    assert modulo != 0
                    return sum([self.encoder.int(value=0).iff(aa[i], self ** i) for i in range(self.bits.bit_length())]) % modulo
                return sum([self.encoder.int(value=0).iff(aa[i], self ** i) for i in range(self.bits.bit_length())])
            else:
                other = self
                for _ in range(power - 1):
                    other *= self
                if modulo is not None:
                    return other % modulo
                return other

    def __truediv__(self, other):
        if isinstance(other, Atom):
            assert other != 0
        if self.value is not None:
            if isinstance(other, Atom) and other.value is not None:
                if other.value == 0:
                    from math import nan
                    return nan
                return self.value / other.value
        output_block = self.encoder.create_block()
        if isinstance(other, Atom):
            self.encoder.bv_lud_gate(self.block, other.block, output_block, self.encoder.int(value=0).block)
        else:
            self.encoder.bv_lud_gate(self.block, self.encoder.constant(other), output_block, self.encoder.int(value=0).block)
        return Atom(self.encoder, block=output_block)

    def __sub__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value - other.value
            else:
                return self.value - other
        output_block = self.encoder.create_block()
        if isinstance(other, Atom):
            output_block = self.encoder.bv_rcs_gate(self.block, other.block, output_block)
        else:
            output_block = self.encoder.bv_rcs_gate(self.block, self.encoder.constant(other), output_block)
        return Atom(self.encoder, block=output_block)

    def __rsub__(self, other):
        return self - other

    def __lt__(self, other):
        if self.value is not None:
            if isinstance(other, Atom) and other.value is not None:
                return self.value < other.value
            else:
                return self.value < other
        if isinstance(other, Atom):
            self.encoder.bv_ule_gate(other.block, self.block, self.encoder.true)
        else:
            self.encoder.bv_ule_gate(self.encoder.constant(other), self.block, self.encoder.true)
        return self

    def __le__(self, other):
        return self.__lt__(other + 1)

    def __gt__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value > other.value
            else:
                return self.value > other
        if isinstance(other, Atom):
            return self.encoder.bv_ule_gate(self.block, other.block, self.encoder.true)
        else:
            return self.encoder.bv_ule_gate(self.block, self.encoder.constant(other), self.encoder.true)

    def __ge__(self, other):
        if other > 0:
            return self.__gt__(other - 1)
        return True

    def __neg__(self):
        if self.value is not None:
            return -self.value
        return self.encoder.int(value=0) - self

    def __abs__(self):
        if self.value is not None:
            return abs(self.value)
        self.encoder.add_block([self.block[-1]])
        return self.iff(-self.block[-1], -self)

    def __and__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value & other.value
            else:
                return self.value & other
        if isinstance(other, Atom):
            output_block = self.encoder.bv_and_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_and_gate(self.block, self.encoder.constant(other))
        return Atom(self.encoder, block=output_block)

    def __or__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value | other.value
            else:
                return self.value | other
        if isinstance(other, Atom):
            output_block = self.encoder.bv_or_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_or_gate(self.block, self.encoder.constant(other))
        return Atom(self.encoder, block=output_block)

    def __xor__(self, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value ^ other.value
            else:
                return self.value ^ other
        if isinstance(other, Atom):
            output_block = self.encoder.bv_xor_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_xor_gate(self.block, self.encoder.constant(other))
        return Atom(self.encoder, block=output_block)

    def __lshift__(self, other):
        if isinstance(other, Atom):
            assert 0 < other
        y = 2 * other
        x = self * y
        return x

    def __rshift__(self, other):
        if isinstance(other, Atom):
            assert 0 < other
        y = 2 * other
        x = self / y
        return x

    def iff(self, bit, other):
        if self.value is not None:
            if isinstance(other, Atom):
                return self.value if bit else other.value
            else:
                return self.value if bit else other
        if isinstance(bit, Atom):
            import functools
            import operator
            if isinstance(other, Atom):
                return self.iff(functools.reduce(operator.and_, [self.encoder.int(value=0).iff(bit[j], 1) for j in range(self.encoder.bits)])[0], other)
            else:
                return self.iff(functools.reduce(operator.and_, [self.encoder.int(value=0).iff(bit[j], 1) for j in range(self.encoder.bits)])[0], self.encoder.constant(other))
        if isinstance(other, Atom):
            output_block = self.encoder.bv_mux_gate(self.block, other.block, bit)
            return Atom(self.encoder, block=output_block)
        else:
            output_block = self.encoder.bv_mux_gate(self.block, self.encoder.constant(other), bit)
            return Atom(self.encoder, block=output_block)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        bb = self.data[:]
        for i in item:
            bb = bb[i]
        return lambda a, b: (a if isinstance(a, Atom) else self.encoder.int(value=a)).iff(-bb, (b if isinstance(b, Atom) else self.encoder.int(value=b)))

    @property
    def binary(self):
        def __encode(n):
            if self.bin:
                return self.bin
            bits = []
            n = abs(n)
            for i in range(self.bits):
                if n % 2 == 0:
                    bits += [False]
                else:
                    bits += [True]
                n //= 2
            self.bin = bits
            return bits

        return self.encoder.reshape(__encode(self.value), self.deep)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.__repr__())

    def __int__(self):
        return int(self.__repr__())

    def __float__(self):
        return float(self.__repr__())
