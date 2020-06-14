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


class Linear:
    def __init__(self, encoder, idx, key=None, is_real=False):
        self.key = key
        self.encoder = encoder
        self.value = None
        self.is_real = is_real
        self.idx = idx
        self.value = 1
        self.constraint = [self]

    def __add__(self, other):
        self.constraint += other.constraint
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        return self + other

    def __eq__(self, other):
        self.constraint.append('==')
        self.constraint.append(other)
        self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
        del self.constraint[:]
        self.constraint.append(self)
        self.value = 1
        return True

    def __mul__(self, other):
        self.value *= other
        return self

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        if isinstance(other, Linear):
            other.value = -other.value
        self.constraint += other.constraint
        return self

    def __rsub__(self, other):
        return self - other

    def __le__(self, other):
        self.constraint.append('<=')
        self.constraint.append(other)
        self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
        del self.constraint[:]
        self.constraint.append(self)
        self.value = 1
        return True

    def __ge__(self, other):
        self.constraint.append('>=')
        self.constraint.append(other)
        self.encoder.add_constraint(self.constraint[:-2], self.constraint[-2], self.constraint[-1])
        del self.constraint[:]
        self.constraint.append(self)
        self.value = 1
        return True

    def __neg__(self):
        return -1 * self

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.__repr__())

    def __int__(self):
        return int(float(self.__repr__()))

    def __float__(self):
        return float(self.__repr__())
