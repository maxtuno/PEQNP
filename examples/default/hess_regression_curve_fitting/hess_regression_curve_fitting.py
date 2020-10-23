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

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import peqnp as cnf
from sklearn.metrics import mean_tweedie_deviance
from sklearn.preprocessing import MinMaxScaler

top = np.inf


def oracle(seq):
    global W, X, Y, top
    w = W[seq][:m]
    error = 0
    for x, y in zip(X, Y):
        error += (np.dot(x, w) - y[0]) ** 2
        if error > top:
            return error
    if error < top:
        top = error
        print(top)
    return error / len(X)


if __name__ == '__main__':
    # seed
    np.random.seed(0)

    car_df = pd.read_csv('Car_Purchasing_Data.csv', encoding='ISO-8859-1')
    scaler = MinMaxScaler()
    X = scaler.fit_transform(car_df.drop(['Customer Name', 'Customer e-mail', 'Country', 'Car Purchase Amount'], axis=1))
    Y = scaler.fit_transform(car_df['Car Purchase Amount'].values.reshape(-1, 1))

    n, m = 100, len(X[0])
    W = np.random.sample(size=n)
    ini = time.time()
    seq = cnf.hess_sequence(n, oracle=oracle, fast=False)
    end = time.time()
    w = W[seq][:m]

    print(w)

    out = []
    for x in X:
        out.append(np.dot(x, w))

    plt.figure(figsize=(10, 10))
    plt.title('HESS curve fitting time {}s | Mean squared error {}'.format(round(end - ini, 4), mean_tweedie_deviance(out, Y)))
    plt.plot(range(len(X)), out, 'r-', label='HESS', alpha=0.7)
    plt.plot(range(len(X)), Y, 'g-', label='Real', alpha=0.7)
    plt.legend()
    plt.show()
