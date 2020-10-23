///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef SLIME_SAT_SOLVER_SLIME_HH
#define SLIME_SAT_SOLVER_SLIME_HH

#include <Python.h>
#include "pixie.hh"

pixie *mip;
result res;

PyObject *reset(PyObject *self, PyObject *args) {
    delete mip;
    mip = new pixie();
    Py_RETURN_NONE;
}

PyObject *add_objective(PyObject *self, PyObject *args) {
    PyObject *pList;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    std::vector<double> constraint;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        PyObject *pItem = PyList_GetItem(pList, i);
        double var = PyFloat_AsDouble(pItem);
        // Py_DECREF(pItem);
        constraint.push_back(var);
    }
    // TODO: Fix
    // Py_DECREF(pList);

    mip->add_objective(constraint);

    Py_RETURN_NONE;
}

PyObject *set_integer_condition(PyObject *self, PyObject *args) {
    PyObject *pList;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    std::vector<bool> constraint;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        PyObject *pItem = PyList_GetItem(pList, i);
        int var = PyLong_AsLong(pItem);
        // Py_DECREF(pItem);
        constraint.push_back(var == 1);
    }
    // Py_DECREF(pList);

    mip->set_integer_condition(constraint);

    Py_RETURN_NONE;
}

PyObject *add_constraint(PyObject *self, PyObject *args) {
    PyObject *pList;

    char *s;
    double d;

    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!sd", &PyList_Type, &pList, &s, &d)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    std::vector<double> constraint;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        PyObject *pItem = PyList_GetItem(pList, i);
        double var = PyFloat_AsDouble(pItem);
        // Py_DECREF(pItem);
        constraint.push_back(var);
    }
    // Py_DECREF(pList);

    mip->add_constraint(constraint, s, d);

    Py_RETURN_NONE;
}

PyObject *minimize(PyObject *self, PyObject *args) {
    bool solve;
    char *path;
    if (!PyArg_ParseTuple(args, "bs", &solve, &path)) {
        Py_RETURN_NONE;
    }
    if (strcmp(path, "") != 0) {
        mip->put(path);
    }
    if (solve) {
        res = mip->optimize();
        PyObject *modelList = PyList_New(res.get_variables().size());
        for (unsigned int i = 0; i < res.get_variables().size(); i++) {
            PyList_SetItem(modelList, i, PyFloat_FromDouble(res.get_variables()[i]));
        }
        return modelList;
    }
    Py_RETURN_NONE;
}

PyObject *maximize(PyObject *self, PyObject *args) {
    bool solve;
    char *path;
    if (!PyArg_ParseTuple(args, "bs", &solve, &path)) {
        Py_RETURN_NONE;
    }
    if (strcmp(path, "") != 0) {
        mip->put(path);
    }
    if (solve) {
        res = mip->optimize();
        PyObject *modelList = PyList_New(res.get_variables().size());
        for (unsigned int i = 0; i < res.get_variables().size(); i++) {
            PyList_SetItem(modelList, i, PyFloat_FromDouble(res.get_variables()[i]));
        }
        return modelList;
    }
    Py_RETURN_NONE;
}

PyObject *optimal(PyObject *self, PyObject *args) {
    return PyFloat_FromDouble(res.get_optimal());
}

#endif //SLIME_SAT_SOLVER_SLIME_HH
