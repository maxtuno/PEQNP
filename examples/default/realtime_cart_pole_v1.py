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

import gym
import numpy as np
import peqnp as cnf


def run_episode(seq, render=False):
    global par, m, env
    par = par[seq]
    observation = env.reset()
    total_reward = 0
    for _ in range(m):
        if render:
            env.render()
        action = 0 if np.matmul(par, observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            break
    env.close()
    return m - total_reward


if __name__ == '__main__':

    env = gym.make('CartPole-v1')

    n = 4
    m = 500
    glb = np.inf
    while True:
        par = np.random.sample(size=n)
        seq = cnf.hess_sequence(n, oracle=run_episode, fast=False)
        loc = run_episode(seq)
        if loc < glb:
            glb = loc
            print(glb, par)
            if glb == 0:
                if run_episode(seq, render=True) == 0:
                    break
                else:
                    glb = np.inf
