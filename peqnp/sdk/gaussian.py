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

from .entity import *


class Gaussian:
    def __init__(self, x, y):
        self.real = x
        self.imag = y

    def __eq__(self, other):
        assert self.real == other.real
        assert self.imag == other.imag
        return True

    def __ne__(self, other):
        bit = Entity(self.real.encoder, bits=2)
        assert (self.real - other.real).iff(bit[0], self.imag - other.imag) != 0
        return True

    def __neg__(self):
        return Gaussian(-self.real, -self.imag)

    def __add__(self, other):
        return Gaussian(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Gaussian(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Gaussian((self.real * other.real) - (self.imag * other.imag), ((self.real * other.imag) + (self.imag * other.real)))

    def __truediv__(self, other):
        return Gaussian(((self.real * other.real) + (self.imag * other.imag)) / (other.real ** 2 + other.imag ** 2), ((self.imag * other.real) - (self.real * other.imag)) / (other.real ** 2 + other.imag ** 2))

    def __pow__(self, power, modulo=None):
        if isinstance(power, Entity):
            slots = Entity(power.encoder, bits=power.encoder.deep)
            assert sum([power.encoder.zero.iff(slots[i], 1) for i in range(power.encoder.deep)]) == 1
            assert sum([power.encoder.zero.iff(slots[i], i) for i in range(power.encoder.deep)]) == power
            return sum([Gaussian(power.encoder.zero.iff(slots[i], 1), 0) * (self ** i) for i in range(power.encoder.deep)])
        else:
            other = self
            for _ in range(power - 1):
                other *= self
            return other

    def __abs__(self):
        return Gaussian(self.real.encoder.sqrt(self.real ** 2 + self.imag ** 2), 0)

    def __repr__(self):
        return '({}+{}j)'.format(self.real, self.imag)

    def __str__(self):
        return str(self.__repr__())

    def __complex__(self):
        return complex(int(self.real), int(self.imag))

    def conjugate(self):
        return Gaussian(self.real, -self.imag)
