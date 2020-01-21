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


class Entity:
    def __init__(self, encoder, key=None, block=None, value=None, bits=None, is_mip=False, is_real=False, idx=None):
        self.key = key
        self.model = []
        self.block = block
        self.encoder = encoder
        self.value = None
        self.is_mip = is_mip
        self.is_real = is_real
        if self.is_mip:
            self.idx = idx
            self.value = 1
            self.constraint = [self]
        if bits is None:
            self.bits = self.encoder.bits
        else:
            self.bits = bits
        if block is None and bits is None and value is None:
            self.key, self.block = self.encoder.create_variable(self.key)
        elif block is None and bits is not None and value is None:
            self.key, self.block = self.encoder.create_variable(self.key, bits)
        elif value is not None:
            self.block = self.encoder.create_constant(value)
        else:
            self.block = block

    def __add__(self, other):
        if self.is_mip:
            if not self.constraint:
                self.constraint.append(self)
            if isinstance(other, Entity):
                self.constraint += other.constraint
            return self
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value + other.value
            return self.value + other
        output_block = self.encoder.create_block()
        if isinstance(other, Entity):
            self.encoder.bv_rca_gate(self.block, other.block, self.encoder.true, output_block, self.encoder.true)
        else:
            self.encoder.bv_rca_gate(self.block, self.encoder.create_constant(other), self.encoder.true, output_block, self.encoder.true)
        return Entity(self.encoder, block=output_block)

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if self.is_mip:
            self.constraint.append('==')
            self.constraint.append(other)
            self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
            self.constraint.clear()
            return True
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value == other.value
            else:
                return self.value == other
        if isinstance(other, Entity):
            return self.encoder.bv_eq_gate(self.block, other.block, self.encoder.false)
        return self.encoder.bv_eq_gate(self.block, self.encoder.create_constant(other), self.encoder.false)

    def __mod__(self, other):
        assert other != 0
        if self.value is not None and other.value is not None:
            return self.value % other.value
        if self.value is not None and other.value is None:
            return self.value % other
        output_block = self.encoder.create_block()
        if isinstance(other, Entity):
            self.encoder.bv_lur_gate(self.block, other.block, output_block)
        else:
            self.encoder.bv_lur_gate(self.block, self.encoder.create_constant(other), output_block)
        return Entity(self.encoder, block=output_block)

    def __ne__(self, other):
        if isinstance(other, Entity):
            return self.encoder.bv_eq_gate(self.block, other.block, self.encoder.true)
        return self.encoder.bv_eq_gate(self.block, self.encoder.create_constant(other), self.encoder.true)

    def __mul__(self, other):
        if self.is_mip:
            self.value *= other
            self.constraint.append(self)
            return self
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value * other.value
            return self.value * other
        output_block = self.encoder.create_block()
        if isinstance(other, Entity):
            self.encoder.bv_pm_gate(self.block, other.block, output_block, self.encoder.true)
        else:
            self.encoder.bv_pm_gate(self.block, self.encoder.create_constant(other), output_block, self.encoder.true)
        return Entity(self.encoder, block=output_block)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        if self.value is not None and not isinstance(power, Entity):
            return self.value ** power
        elif self.value is not None and power.value is not None:
            if modulo is not None:
                return pow(self.value, power.value, modulo)
            return self.value ** power.value
        else:
            if isinstance(power, Entity):
                aa = Entity(self.encoder, bits=self.encoder.bits)
                assert sum([self.encoder.zero.iff(aa[i], 1) for i in range(self.encoder.bits // 2)]) == 1
                assert sum([self.encoder.zero.iff(aa[i], i) for i in range(self.encoder.bits // 2)]) == power
                if modulo is not None:
                    assert modulo != 0
                    return sum([self.encoder.zero.iff(aa[i], self ** i) for i in range(self.encoder.bits // 2)]) % modulo
                return sum([self.encoder.zero.iff(aa[i], self ** i) for i in range(self.encoder.bits // 2)])
            else:
                other = 1
                for _ in range(power):
                    other *= self
                if modulo is not None:
                    return other % modulo
                return other

    def __truediv__(self, other):
        if isinstance(other, Entity):
            assert other != 0
        if self.value is not None:
            if isinstance(other, Entity) and other.value is not None:
                if other.value == 0:
                    from math import nan
                    return nan
                return self.value / other.value
        output_block = self.encoder.create_block()
        if isinstance(other, Entity):
            self.encoder.bv_lud_gate(self.block, other.block, output_block, self.encoder.zero.block)
        else:
            self.encoder.bv_lud_gate(self.block, self.encoder.create_constant(other), output_block, self.encoder.zero.block)
        return Entity(self.encoder, block=output_block)

    def __sub__(self, other):
        if self.is_mip:
            if not self.constraint:
                self.constraint.append(self)
            other.value = -other.value
            self.constraint += other.constraint
            return self
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value - other.value
            else:
                return self.value - other
        output_block = self.encoder.create_block()
        if isinstance(other, Entity):
            output_block = self.encoder.bv_rcs_gate(self.block, other.block, output_block)
        else:
            output_block = self.encoder.bv_rcs_gate(self.block, self.encoder.create_constant(other), output_block)
        return Entity(self.encoder, block=output_block)

    def __rsub__(self, other):
        return self - other

    def __lt__(self, other):
        if self.value is not None:
            if isinstance(other, Entity) and other.value is not None:
                return self.value < other.value
            else:
                return self.value < other
        if isinstance(other, Entity):
            self.encoder.bv_ule_gate(other.block, self.block, self.encoder.true)
        else:
            self.encoder.bv_ule_gate(self.encoder.create_constant(other), self.block, self.encoder.true)
        return self

    def __le__(self, other):
        if self.is_mip:
            if not self.constraint:
                self.constraint.append(self)
            self.constraint.append('<=')
            self.constraint.append(other)
            self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
            self.constraint.clear()
            return True
        return self.__lt__(other + 1)

    def __gt__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value > other.value
            else:
                return self.value > other
        if isinstance(other, Entity):
            return self.encoder.bv_ule_gate(self.block, other.block, self.encoder.true)
        else:
            return self.encoder.bv_ule_gate(self.block, self.encoder.create_constant(other), self.encoder.true)

    def __ge__(self, other):
        if self.is_mip:
            if not self.constraint:
                self.constraint.append(self)
            self.constraint.append('>=')
            self.constraint.append(other)
            self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
            self.constraint.clear()
            return True
        if other > 0:
            return self.__gt__(other - 1)
        return True

    def __neg__(self):
        if self.is_mip:
            self.value = -self.value
        if self.value is not None:
            return -self.value
        return self.encoder.zero - self

    def __abs__(self):
        if self.value is not None:
            return abs(self.value)
        self.encoder.add_block([self.block[-1]])
        return self.iff(-self.block[-1], -self)

    def __and__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value & other.value
            else:
                return self.value & other
        if isinstance(other, Entity):
            output_block = self.encoder.bv_and_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_and_gate(self.block, self.encoder.create_constant(other))
        return Entity(self.encoder, block=output_block)

    def __or__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value | other.value
            else:
                return self.value | other
        if isinstance(other, Entity):
            output_block = self.encoder.bv_or_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_or_gate(self.block, self.encoder.create_constant(other))
        return Entity(self.encoder, block=output_block)

    def __xor__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value ^ other.value
            else:
                return self.value ^ other
        if isinstance(other, Entity):
            output_block = self.encoder.bv_xor_gate(self.block, other.block)
        else:
            output_block = self.encoder.bv_xor_gate(self.block, self.encoder.create_constant(other))
        return Entity(self.encoder, block=output_block)

    def __lshift__(self, other):
        if isinstance(other, Entity):
            assert 0 < other
        y = 2 * other
        x = self * y
        return x

    def __rshift__(self, other):
        if isinstance(other, Entity):
            assert 0 < other
        y = 2 * other
        x = self / y
        return x

    def iff(self, bit, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value if bit else other.value
            else:
                return self.value if bit else other
        if isinstance(bit, Entity):
            import functools
            import operator
            if isinstance(other, Entity):
                return self.iff(functools.reduce(operator.and_, [self.encoder.zero.iff(bit[j], 1) for j in range(self.encoder.bits)])[0], other)
            else:
                return self.iff(functools.reduce(operator.and_, [self.encoder.zero.iff(bit[j], 1) for j in range(self.encoder.bits)])[0], self.encoder.create_constant(other))
        if isinstance(other, Entity):
            output_block = self.encoder.bv_mux_gate(self.block, other.block, bit)
            return Entity(self.encoder, block=output_block)
        else:
            output_block = self.encoder.bv_mux_gate(self.block, self.encoder.create_constant(other), bit)
            return Entity(self.encoder, key=str(other), block=output_block)

    def __getitem__(self, item):
        if self.value is not None:
            def __encode(n):
                i, data = 0, n * [False]
                while n:
                    if n % 2 == 0:
                        data[i] = [True]
                    n //= 2
                    i += 1
                return data

            return __encode(abs(self.value))[item]
        return self.block[item]

    @property
    def binary(self):
        def __encode(n):
            bits = []
            n = abs(n)
            for i in range(self.bits):
                if n % 2 == 0:
                    bits += [False]
                else:
                    bits += [True]
                n //= 2
            return bits

        return __encode(self.value)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.__repr__())

    def __int__(self):
        return int(self.__repr__())

    def __float__(self):
        return float(self.__repr__())
