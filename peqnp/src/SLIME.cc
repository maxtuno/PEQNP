///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp-lib.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include "SLIME.hh"

#if PY_MAJOR_VERSION >= 3
static PyMethodDef module_methods[] = {{"add_clause", (PyCFunction) add_clause, METH_VARARGS, """"""},
                                       {"solve", (PyCFunction) solve, METH_VARARGS, """"""},
                                       {"reset", (PyCFunction) reset, METH_VARARGS, """"""},
                                       {NULL, NULL, 0, NULL}};

static struct PyModuleDef slime = {PyModuleDef_HEAD_INIT, "slime", """SLIME 3 SAT Solver.""", -1, module_methods};

PyMODINIT_FUNC PyInit_slime() {
    return PyModule_Create(&slime);
}

#endif