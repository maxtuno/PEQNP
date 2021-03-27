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

import pandas as pd
import peqnp as pn


def clean(df, lc):
    return df[~df['Name'].isin(lc)]


if __name__ == "__main__":

    # Local example only [:few] pokemon delete this on a powerful machine.
    data = pd.read_csv('data/pokemon_data.csv')[:50]

    done = False
    clusters = []
    latest_cluster = []
    while True:
        data = clean(data[:], latest_cluster)
        if len(data) == 1:
            break
        bits = int(max(data['HP'].sum(),
                       data['Attack'].sum(),
                       data['Defense'].sum(),
                       data['Sp. Atk'].sum(),
                       data['Sp. Def'].sum(),
                       data['Speed'].sum())).bit_length() + 1
        size = len(data)
        goal_a = 0
        goal_b = 0
        goal_c = 0
        goal_d = 0
        goal_e = 0
        goal_f = 0
        while True:
            pn.engine(bits)
            aa, a = pn.subsets(data['HP'].to_numpy().flatten())
            bb, b = pn.subsets(data['Attack'].to_numpy().flatten())
            cc, c = pn.subsets(data['Defense'].to_numpy().flatten())
            dd, d = pn.subsets(data['Sp. Atk'].to_numpy().flatten())
            ee, e = pn.subsets(data['Sp. Def'].to_numpy().flatten())
            ff, f = pn.subsets(data['Speed'].to_numpy().flatten())
            assert aa == bb == cc == dd == ee == ff
            assert sum(a) >= goal_a
            assert sum(b) >= goal_b
            assert sum(c) >= goal_c
            assert sum(d) >= goal_d
            assert sum(e) >= goal_e
            assert sum(f) >= goal_f
            assert 0 < sum(aa[[i]](0, 1) for i in range(len(data))) < size
            if pn.satisfy(turbo=True):
                goal_a = sum([data['HP'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                goal_b = sum([data['Attack'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                goal_c = sum([data['Defense'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                goal_d = sum([data['Sp. Atk'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                goal_e = sum([data['Sp. Def'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                goal_f = sum([data['Speed'].iloc[i] for i in range(len(data)) if aa.binary[i]])
                size = sum(aa.binary)
                print(80 * '-')
                print('HP      :', goal_a)
                print('Attack  :', goal_b)
                print('Defense :', goal_c)
                print('Sp. Atk :', goal_d)
                print('Sp. Def :', goal_e)
                print('Speed   :', goal_f)
                print('Size    :', size)
                aux = []
                for i in range(len(data)):
                    if not aa.binary[i]:
                        aux.append(data['Name'].iloc[i])
                print(aux)
                latest_cluster = aux + [goal_a + goal_b + goal_c + goal_d + goal_f + goal_e]
            else:
                clusters.append(latest_cluster)
                break

    print(80 * '=')
    for i, cluster in enumerate(clusters):
        power, team = cluster[-1], cluster[:-1]
        print('Nº {}'.format(i + 1))
        print('POWER : {}'.format(power))
        print('SIZE  : {}'.format(len(team)))
        print('TEAM  : {}'.format(', '.join(team)))
        print()
    print(80 * '-')
    print('NAME  : {}'.format(data['Name'].iloc[0]))
    print('POWER : {}'.format(data['HP'].iloc[0] +
                            data['Attack'].iloc[0] +
                            data['Defense'].iloc[0] +
                            data['Sp. Atk'].iloc[0] +
                            data['Sp. Def'].iloc[0] +
                            data['Speed'].iloc[0]))
    print(80 * '=')
