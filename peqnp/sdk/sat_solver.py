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

import ctypes


class SATSolver:
    def __init__(self, sat_solver_path):
        self.library = ctypes.cdll.LoadLibrary(sat_solver_path)
        self.version = self.init()
        self.vars = 0

    def description(self):
        self.peqnp_sat_description = self.library.peqnp_sat_description
        self.peqnp_sat_description.restype = ctypes.c_char_p
        return self.library.peqnp_sat_description().decode()

    def init(self):
        self.peqnp_sat_init = self.library.peqnp_sat_init
        self.peqnp_sat_init.restype = ctypes.c_void_p
        self.solver = self.peqnp_sat_init()
        return self.description()

    def release(self):
        self.peqnp_sat_release = self.library.peqnp_sat_release
        self.peqnp_sat_release.argtypes = [ctypes.c_void_p]
        self.peqnp_sat_release.restype = ctypes.c_void_p
        return self.peqnp_sat_release(self.solver)

    def add(self, lit):
        self.peqnp_sat_add = self.library.peqnp_sat_add
        self.peqnp_sat_add.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.peqnp_sat_add.restype = ctypes.c_void_p
        if abs(lit) > self.vars:
            self.vars = abs(lit)
        return self.peqnp_sat_add(self.solver, lit)

    def assume(self, lit):
        self.peqnp_sat_assume = self.library.peqnp_sat_assume
        self.peqnp_sat_assume.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.peqnp_sat_assume.restype = ctypes.c_void_p
        return self.peqnp_sat_assume(self.solver, lit)

    def solve(self, option):
        self.peqnp_sat_solve = self.library.peqnp_sat_solve
        self.peqnp_sat_solve.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.peqnp_sat_solve.restype = ctypes.c_void_p
        res = self.peqnp_sat_solve(self.solver, option.encode())
        if res == 10:
            model = []
            for i in range(1, self.vars + 1):
                model.append(self.val(i))
            return model
        return []

    def val(self, lit):
        self.peqnp_sat_val = self.library.peqnp_sat_val
        self.peqnp_sat_val.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.peqnp_sat_val.restype = ctypes.c_int
        return self.library.peqnp_sat_val(self.solver, lit)
