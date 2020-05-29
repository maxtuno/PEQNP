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


class MIPSolver:
    def __init__(self, mip_solver_path):
        self.library = ctypes.cdll.LoadLibrary(mip_solver_path)
        self.version = self.init()

    def description(self):
        self.peqnp_mip_description = self.library.peqnp_mip_description
        self.peqnp_mip_description.restype = ctypes.c_char_p
        return self.library.peqnp_mip_description().decode()

    def init(self):
        self.peqnp_mip_init = self.library.peqnp_mip_init
        self.peqnp_mip_init.restype = ctypes.c_void_p
        self.solver = self.peqnp_mip_init()
        return self.description()

    def set_objective(self, values):
        self.peqnp_mip_set_objective = self.library.peqnp_mip_set_objective
        self.peqnp_mip_set_objective.argtypes = [ctypes.c_void_p, ctypes.c_double * len(values), ctypes.c_int]
        self.peqnp_mip_set_objective.restype = ctypes.c_void_p
        self.solver = self.peqnp_mip_set_objective(self.solver, (ctypes.c_double * len(values))(*values), len(values))
        return self.solver

    def add_constraint(self, values, comparator, rigth):
        if comparator == '<=':
            comparator = -1
        elif comparator == '>=':
            comparator = 1
        elif comparator == '==':
            comparator = 0
        self.peqnp_mip_add_constraint = self.library.peqnp_mip_add_constraint
        self.peqnp_mip_add_constraint.argtypes = [ctypes.c_void_p, ctypes.c_double * len(values), ctypes.c_int, ctypes.c_double, ctypes.c_int]
        self.peqnp_mip_add_constraint.restype = ctypes.c_void_p
        self.solver = self.peqnp_mip_add_constraint(self.solver, (ctypes.c_double * len(values))(*values), comparator, rigth, len(values))
        return self.solver

    def set_integer_condition(self, values):
        self.peqnp_mip_set_integer_condition = self.library.peqnp_mip_set_integer_condition
        self.peqnp_mip_set_integer_condition.argtypes = [ctypes.c_void_p, ctypes.c_int * len(values), ctypes.c_int]
        self.peqnp_mip_set_integer_condition.restype = ctypes.c_void_p
        self.solver = self.peqnp_mip_set_integer_condition(self.solver, (ctypes.c_int * len(values))(*values), len(values))
        return self.solver

    def maximize(self):
        self.peqnp_mip_maximize = self.library.peqnp_mip_maximize
        self.peqnp_mip_maximize.argtypes = [ctypes.c_void_p]
        self.peqnp_mip_maximize.restype = ctypes.c_double
        return self.library.peqnp_mip_maximize(self.solver)

    def val(self, idx):
        self.peqnp_mip_val = self.library.peqnp_mip_val
        self.peqnp_mip_val.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.peqnp_mip_val.restype = ctypes.c_double
        return self.library.peqnp_mip_val(self.solver, idx)
