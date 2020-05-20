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


class Rational:
    def __init__(self, x, y):
        self.denominator = x
        self.numerator = y
        assert self.numerator > 0

    def __eq__(self, other):
        if isinstance(other, Entity):
            assert self.denominator == other
            assert self.numerator == 1
        else:
            assert self.denominator == other.denominator
            assert self.numerator == other.numerator
        return True

    def __ne__(self, other):
        assert self.denominator * other.numerator != self.numerator * other.denominator
        return True

    def __neg__(self):
        return Rational(-self.denominator, self.numerator)

    def __add__(self, other):
        return Rational(self.denominator * other.numerator + self.numerator * other.denominator, self.numerator * other.numerator)

    def __radd__(self, other):
        if other == 0:
            return self
        return self + other

    def __sub__(self, other):
        return Rational(self.denominator * other.numerator - self.numerator * other.denominator, self.numerator * other.numerator)

    def __mul__(self, other):
        if isinstance(other, Entity):
            return Rational(self.denominator * other, self.numerator)
        return Rational(self.denominator * other.denominator, self.numerator * other.numerator)

    def __truediv__(self, other):
        return self * other.invert()

    def __le__(self, other):
        if isinstance(other, Entity):
            assert self.numerator * other >= self.denominator
        else:
            assert self.numerator * other.denominator >= self.denominator * other.numerator
        return True

    def __ge__(self, other):
        if isinstance(other, Entity):
            assert self.numerator <= other * self.denominator
        else:
            assert self.numerator * other.denominator <= self.denominator * other.numerator
        return True

    def __lt__(self, other):
        if isinstance(other, Entity):
            assert self.numerator * other > self.denominator
        else:
            assert self.numerator * other.denominator > self.denominator * other.numerator
        return True

    def __gt__(self, other):
        if isinstance(other, Entity):
            assert self.numerator < other * self.denominator
        else:
            assert self.numerator * other.denominator < self.denominator * other.numerator
        return True

    def __pow__(self, power, modulo=None):
        if isinstance(power, Entity):
            slots = Entity(power.encoder, bits=power.encoder.deep)
            assert sum([power.encoder.zero.iff(slots[i], 1) for i in range(power.encoder.deep)]) == 1
            assert sum([power.encoder.zero.iff(slots[i], i) for i in range(power.encoder.deep)]) == power
            return sum([(self ** i) * power.encoder.zero.iff(slots[i], 1) for i in range(power.encoder.deep)])
        else:
            other = self
            for _ in range(power - 1):
                other = other * self
            return other

    def __abs__(self):
        return Rational(abs(self.denominator), abs(self.numerator))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '({} / {})'.format(self.denominator, self.numerator)

    def __float__(self):
        return float(self.denominator) / float(self.numerator)

    def invert(self):
        return Rational(self.numerator, self.denominator)
