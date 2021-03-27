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

# !pip install PEQNP

# ref: http://www.csc.kth.se/~viggo/wwwcompendium/node152.html

import random

import peqnp as pn

bits = 10
n = 2 * 100

D = [random.randint(1, 2 ** bits) for _ in range(n)]

print('D   : {}'.format(D))

pn.engine(sum(D).bit_length())

bins, sub, com = pn.subsets(D, n // 2, complement=True)

assert sum(sub) == sum(com)

if pn.satisfy(turbo=True):
    sub = [D[i] for i in range(n) if bins.binary[i]]
    com = [D[i] for i in range(n) if not bins.binary[i]]
    print(sum(sub), sum(com))
    print(sub, com)
    print('\n')
else:
    print('Infeasible ...')

"""
D   : [1024, 420, 909, 189, 1022, 717, 621, 60, 473, 961, 690, 278, 902, 162, 867, 180, 627, 380, 344, 524, 131, 221, 729, 912, 911, 364, 110, 706, 775, 124, 722, 730, 596, 189, 22, 500, 882, 291, 674, 709, 219, 677, 404, 547, 41, 282, 347, 484, 687, 897, 459, 10, 543, 298, 1015, 818, 268, 804, 660, 403, 144, 824, 985, 987, 1002, 422, 619, 225, 738, 875, 352, 939, 213, 821, 132, 78, 625, 364, 300, 406, 377, 498, 580, 314, 79, 253, 263, 29, 1009, 662, 16, 881, 598, 341, 871, 902, 365, 301, 49, 325, 618, 15, 657, 876, 595, 996, 374, 934, 205, 875, 259, 119, 312, 976, 311, 516, 314, 421, 474, 318, 963, 746, 730, 236, 26, 920, 897, 226, 716, 559, 959, 365, 120, 963, 202, 326, 54, 814, 364, 50, 360, 267, 137, 403, 794, 316, 236, 793, 604, 238, 201, 355, 758, 271, 73, 248, 872, 470, 648, 796, 638, 338, 264, 575, 737, 695, 799, 312, 316, 804, 441, 494, 322, 328, 196, 950, 697, 356, 743, 404, 40, 320, 571, 316, 352, 390, 305, 289, 508, 207, 976, 53, 809, 5, 508, 170, 415, 254, 42, 693]
49074 49074
[420, 473, 690, 278, 902, 162, 344, 729, 912, 911, 110, 722, 730, 189, 500, 882, 291, 674, 709, 677, 404, 547, 484, 10, 804, 403, 985, 987, 1002, 422, 225, 738, 939, 132, 300, 406, 498, 580, 314, 79, 253, 263, 598, 871, 902, 618, 15, 657, 595, 374, 934, 875, 312, 311, 314, 421, 318, 963, 746, 236, 26, 920, 226, 559, 959, 963, 326, 54, 814, 364, 360, 267, 137, 794, 316, 236, 638, 338, 264, 575, 737, 695, 799, 312, 441, 322, 697, 404, 571, 352, 390, 305, 289, 508, 207, 53, 5, 415, 254, 42] [1024, 909, 189, 1022, 717, 621, 60, 961, 867, 180, 627, 380, 524, 131, 221, 364, 706, 775, 124, 596, 22, 219, 41, 282, 347, 687, 897, 459, 543, 298, 1015, 818, 268, 660, 144, 824, 619, 875, 352, 213, 821, 78, 625, 364, 377, 29, 1009, 662, 16, 881, 341, 365, 301, 49, 325, 876, 996, 205, 259, 119, 976, 516, 474, 730, 897, 716, 365, 120, 202, 50, 403, 793, 604, 238, 201, 355, 758, 271, 73, 248, 872, 470, 648, 796, 316, 804, 494, 328, 196, 950, 356, 743, 40, 320, 316, 976, 809, 508, 170, 693]
"""