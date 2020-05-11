///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include "pixie.h"

static PyMethodDef module_methods[] = {{"add_objective", (PyCFunction) add_objective, METH_VARARGS,
                                        ""
                                        ""
                                        ""},
                                       {"add_constraint", (PyCFunction) add_constraint, METH_VARARGS,
                                                ""
                                                ""
                                                ""},
                                       {"set_integer_condition", (PyCFunction) set_integer_condition, METH_VARARGS,
                                               ""
                                               ""
                                               ""},
                                       {"reset", (PyCFunction) reset, METH_VARARGS,
                                               ""
                                               ""
                                               ""},
                                       {"minimize", (PyCFunction) minimize, METH_VARARGS,
                                               ""
                                               ""
                                               ""},
                                       {"maximize", (PyCFunction) maximize, METH_VARARGS,
                                               ""
                                               ""
                                               ""},
                                       {"optimal", (PyCFunction) optimal, METH_VARARGS,
                                               ""
                                               ""
                                               ""},
                                       {NULL, NULL, 0, NULL}};

#if PY_MAJOR_VERSION < 3
    PyMODINIT_FUNC initpixie() {
        Py_InitModule3("pixie", module_methods, "");
    }
#else
    static struct PyModuleDef pixie = {PyModuleDef_HEAD_INIT, "pixie",
                                       ""
                                       "PIXIE 1 MIP Solver."
                                       "",
                                       -1, module_methods};

    PyMODINIT_FUNC PyInit_pixie() {
        return PyModule_Create(&pixie);
    }
#endif