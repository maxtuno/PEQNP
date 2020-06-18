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

import peqnp as pn


def load_prec(file_name):
    data = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            data.append(list(map(int, line.split(' ')[1:])))
    return data


def load_upit(file_name):
    data = []
    with open(file_name) as file:
        lines = file.readlines()
        name = lines[0].replace('NAME: ', '')
        del lines[0]
        _ = lines[0].replace('TYPE:', '')
        del lines[0]
        n_blocks = int(lines[0].replace('NBLOCKS: ', '').strip('\n'))
        del lines[0]
        _ = lines[0].replace('OBJECTIVE_FUNCTION:', '')
        del lines[0]
        for line in lines:
            if line.startswith('EOF'):
                break
            a, b = line.strip('\n').split(' ')
            data.append(float(b))
        return n_blocks, data


if __name__ == '__main__':
    # Remember
    # pip install PEQNP --upgrade

    # Minelib: A library of open-pit mining problems
    # data from http://mansci-web.uai.cl/minelib
    n, upit = load_upit('data/newman1.upit')
    prec = load_prec('data/newman1.prec')

    print('wait for it...')

    pn.engine()
    x = pn.vector(size=n, is_mip=True)
    pn.all_binaries(x)
    for i in range(n):
        for j in prec[i]:
            # Note this, in future versions will support the notation x[i] <= x[j]
            assert x[j] - x[i] >= 0
    # use LP_SOLVE to solve this, is more fast, PIXIE es an small MIP solver (for now)...
    pn.maximize(sum(upit[i] * x[i] for i in range(n)), lp_path='upit.lp', solve=False)
