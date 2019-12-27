"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////
"""


class Entity:
    def __init__(self, encoder, key=None, block=None, value=None, size=None, is_real=False):
        self._key = key
        self._model = []
        self._block = block
        self._encoder = encoder
        self._value = None
        self._is_real = is_real
        if size is None:
            self._size = self._encoder.bits
        else:
            self._size = size
        if block is None and size is None and value is None:
            self._key, self._block = self._encoder.create_variable(self._key)
        elif block is None and size is not None and value is None:
            self._key, self._block = self._encoder.create_variable(self._key, size)
        elif value is not None:
            self._block = self._encoder.create_constant(value)
        else:
            self._block = block

    def __add__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value + other.value
            return self.value + other
        output_block = self._encoder.create_block()
        if isinstance(other, Entity):
            self._encoder.bv_rca_gate(self._block, other._block, self._encoder.true, output_block, self._encoder.true)
        else:
            self._encoder.bv_rca_gate(self._block, self._encoder.create_constant(other), self._encoder.true, output_block, self._encoder.true)
        return Entity(self._encoder, block=output_block)

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value == other.value
            else:
                return self.value == other
        if isinstance(other, Entity):
            return self._encoder.bv_eq_gate(self._block, other._block, self._encoder.false)
        return self._encoder.bv_eq_gate(self._block, self._encoder.create_constant(other), self._encoder.false)

    def __mod__(self, other):
        if self.value is not None and other.value is not None:
            return self.value % other.value
        if self.value is not None and other.value is None:
            return self.value % other
        output_block = self._encoder.create_block()
        if isinstance(other, Entity):
            self._encoder.bv_lur_gate(self._block, other._block, output_block)
        else:
            self._encoder.bv_lur_gate(self._block, self._encoder.create_constant(other), output_block)
        return Entity(self._encoder, block=output_block)

    def __ne__(self, other):
        if isinstance(other, Entity):
            return self._encoder.bv_eq_gate(self._block, other._block, self._encoder.true)
        return self._encoder.bv_eq_gate(self._block, self._encoder.create_constant(other), self._encoder.true)

    def __mul__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value * other.value
            return self.value * other
        output_block = self._encoder.create_block()
        if isinstance(other, Entity):
            self._encoder.bv_pm_gate(self._block, other._block, output_block, self._encoder.true)
        else:
            self._encoder.bv_pm_gate(self._block, self._encoder.create_constant(other), output_block, self._encoder.true)
        return Entity(self._encoder, block=output_block)

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
                aa = Entity(self._encoder, size=self._encoder.deepness)
                assert sum([self._encoder.zero.iff(aa[i], self._encoder.one) for i in range(self._encoder.deepness)]) == self._encoder.one
                assert sum([self._encoder.zero.iff(aa[i], i) for i in range(self._encoder.deepness)]) == power
                if modulo is not None:
                    return sum([self._encoder.zero.iff(aa[i], self ** i) for i in range(self._encoder.deepness)]) % modulo
                return sum([self._encoder.zero.iff(aa[i], self ** i) for i in range(self._encoder.deepness)])
            else:
                other = self._encoder.one
                for _ in range(power):
                    other *= self
                if modulo is not None:
                    return other % modulo
                return other

    def __truediv__(self, other):
        if self.value is not None:
            if isinstance(other, Entity) and other.value is not None:
                return self.value / other.value
        output_block = self._encoder.create_block()
        if isinstance(other, Entity):
            self._encoder.bv_lud_gate(self._block, other._block, output_block, self._encoder.zero._block)
        else:
            self._encoder.bv_lud_gate(self._block, self._encoder.create_constant(other), output_block, self._encoder.zero._block)
        return Entity(self._encoder, block=output_block)

    def __sub__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value - other.value
            else:
                return self.value - other
        output_block = self._encoder.create_block()
        if isinstance(other, Entity):
            output_block = self._encoder.bv_rcs_gate(self._block, other._block, output_block)
        else:
            output_block = self._encoder.bv_rcs_gate(self._block, self._encoder.create_constant(other), output_block)
        return Entity(self._encoder, block=output_block)

    def __rsub__(self, other):
        return self - other

    def __lt__(self, other):
        if self.value is not None:
            if isinstance(other, Entity) and other.value is not None:
                return self.value < other.value
            else:
                return self.value < other
        if isinstance(other, Entity):
            self._encoder.bv_ule_gate(other._block, self._block, self._encoder.true)
        else:
            self._encoder.bv_ule_gate(self._encoder.create_constant(other), self._block, self._encoder.true)
        return self

    def __le__(self, other):
        return self.__lt__(other + self._encoder.one)

    def __gt__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value > other.value
            else:
                return self.value > other
        if isinstance(other, Entity):
            return self._encoder.bv_ule_gate(self._block, other._block, self._encoder.true)
        else:
            return self._encoder.bv_ule_gate(self._block, self._encoder.create_constant(other), self._encoder.true)

    def __ge__(self, other):
        if other > 0:
            return self.__gt__(other - self._encoder.one)
        return True

    def __neg__(self):
        if self.value is not None:
            return -self.value
        self._block[-1] = -self._block[-1]
        return self

    def __abs__(self):
        if self.value is not None:
            return abs(self.value)
        self._encoder.add_block([self._block[-1]])
        return self.iff(-self._block[-1], -self)

    def __and__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value & other.value
            else:
                return self.value & other
        if isinstance(other, Entity):
            output_block = self._encoder.bv_and_gate(self._block, other._block)
        else:
            output_block = self._encoder.bv_and_gate(self._block, self._encoder.create_constant(other))
        return Entity(self._encoder, block=output_block)

    def __or__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value | other.value
            else:
                return self.value | other
        if isinstance(other, Entity):
            output_block = self._encoder.bv_or_gate(self._block, other._block)
        else:
            output_block = self._encoder.bv_or_gate(self._block, self._encoder.create_constant(other))
        return Entity(self._encoder, block=output_block)

    def __xor__(self, other):
        if self.value is not None:
            if isinstance(other, Entity):
                return self.value ^ other.value
            else:
                return self.value ^ other
        if isinstance(other, Entity):
            output_block = self._encoder.bv_xor_gate(self._block, other._block)
        else:
            output_block = self._encoder.bv_xor_gate(self._block, self._encoder.create_constant(other))
        return Entity(self._encoder, block=output_block)

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
                return self.iff(functools.reduce(operator.and_, [self._encoder.zero.iff(bit[j], self._encoder.one) for j in range(self._encoder.bits)])[0], other)
            else:
                return self.iff(functools.reduce(operator.and_, [self._encoder.zero.iff(bit[j], self._encoder.one) for j in range(self._encoder.bits)])[0], self._encoder.create_constant(other))
        if isinstance(other, Entity):
            output_block = self._encoder.bv_mux_gate(self._block, other._block, bit)
            return Entity(self._encoder, block=output_block)
        else:
            output_block = self._encoder.bv_mux_gate(self._block, self._encoder.create_constant(other), bit)
            return Entity(self._encoder, key=str(other), block=output_block)

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
        return self._block[item]

    @property
    def value(self):
        if self._value is not None:
            return self._value
        return None

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def type(self):
        return Entity

    @property
    def size(self):
        return self._size

    @property
    def binary(self):
        def __encode(n):
            bits = []
            n = abs(n)
            for i in range(self._size):
                if n % 2 == 0:
                    bits += [False]
                else:
                    bits += [True]
                n //= 2
            return bits

        return __encode(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)
