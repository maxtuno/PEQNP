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

best = 0
render = False


def run_episode(seq):
    global par, m, n, env, best, render
    observation = env.reset()
    _ = np.zeros_like(observation)
    total_reward = 0
    for action in par[seq]:
        if render:
            env.render()
        observation, reward, done, info = env.step(int(observation.flatten().sum() % action))
        total_reward += reward
        if total_reward > best:
            best = total_reward
            print(best)
            if best >= 10000.0:
                render = True
        if done:
            return 0
    env.close()
    return -total_reward


if __name__ == '__main__':
    m = 100000

    env = gym.make('Solaris-ram-v0')
    n = len(env.unwrapped.get_action_meanings())
    par = np.random.randint(1, n + 1, size=n * m)
    seq = cnf.hess_sequence(n * m, oracle=run_episode, fast=False)
