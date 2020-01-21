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

peqnp::science::pixie<double> *mip;
peqnp::science::result<double> result;

PyObject *reset(PyObject *self, PyObject *args) {
    delete mip;
    mip = new peqnp::science::pixie<double>();
    Py_RETURN_NONE;
}

PyObject *add_objective(PyObject *self, PyObject *args) {
    PyObject *pList;
    PyObject *pItem;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    std::vector<double> constraint;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        pItem = PyList_GetItem(pList, i);
        double var = PyFloat_AsDouble(pItem);
        constraint.push_back(var);
    }

    mip->add_objective(constraint);

    Py_RETURN_NONE;
}

PyObject *set_integer_condition(PyObject *self, PyObject *args) {
    PyObject *pList;
    PyObject *pItem;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    std::vector<bool> constraint;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        pItem = PyList_GetItem(pList, i);
        int var = PyLong_AsLong(pItem);
        constraint.push_back(var == 1);
    }

    mip->set_integer_condition(constraint);

    Py_RETURN_NONE;
}

PyObject *add_constraint(PyObject *self, PyObject *args) {
    PyObject *pList;
    PyObject *pItem;

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
        pItem = PyList_GetItem(pList, i);
        double var = PyFloat_AsDouble(pItem);
        constraint.push_back(var);
    }

    mip->add_constraint(constraint, s, d);

    Py_RETURN_NONE;
}

PyObject *minimize(PyObject *self, PyObject *args) {
    result = mip->optimize();
    PyObject *modelList = PyList_New(result.get_variables().size());
    for (unsigned int i = 0; i < result.get_variables().size(); i++) {
        PyList_SetItem(modelList, i, PyFloat_FromDouble(result.get_variables()[i]));
    }
    return modelList;
}

PyObject *maximize(PyObject *self, PyObject *args) {
    result = mip->optimize();
    PyObject *modelList = PyList_New(result.get_variables().size());
    for (unsigned int i = 0; i < result.get_variables().size(); i++) {
        PyList_SetItem(modelList, i, PyFloat_FromDouble(result.get_variables()[i]));
    }
    return modelList;
}

PyObject *optimal(PyObject *self, PyObject *args) {
    return PyFloat_FromDouble(result.get_optimal());
}

#endif //SLIME_SAT_SOLVER_SLIME_HH
