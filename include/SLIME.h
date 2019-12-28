///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef SLIME_SAT_SOLVER_SLIME_HH
#define SLIME_SAT_SOLVER_SLIME_HH

#include <Dimacs.h>
#include <Python.h>
#include <SimpSolver.h>
#include <SolverTypes.h>

using namespace SLIME;

SimpSolver *S;
int v;

#if _WIN32 || _WIN64
void printHeader() {
    printf("                                             \n");
    printf(" SLIME SAT Solver by http://www.peqnp.science\n");
    printf("                                             \n");
}
#else
void printHeader() {
    printf("c                                          \n");
    printf("c    ██████  ██▓     ██▓ ███▄ ▄███▓▓█████  \n");
    printf("c  ▒██    ▒ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▓█   ▀  \n");
    printf("c  ░ ▓██▄   ▒██░    ▒██▒▓██    ▓██░▒███    \n");
    printf("c    ▒   ██▒▒██░    ░██░▒██    ▒██ ▒▓█  ▄  \n");
    printf("c  ▒██████▒▒░██████▒░██░▒██▒   ░██▒░▒████▒ \n");
    printf("c  ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░░░ ▒░ ░ \n");
    printf("c  ░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░░  ░      ░ ░ ░  ░ \n");
    printf("c  ░  ░  ░    ░ ░    ▒ ░░      ░      ░    \n");
    printf("c        ░      ░  ░ ░         ░      ░  ░ \n");
    printf("c                                          \n");
    printf("c         http://www.slime.science         \n");
    printf("c                                          \n");
}
#endif

PyObject *reset(PyObject *self, PyObject *args) {
    delete S;
    S = new SimpSolver();

    Py_RETURN_NONE;
}

PyObject *add_clause(PyObject *self, PyObject *args) {
    PyObject *pList;
    PyObject *pItem;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    vec<Lit> clause;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        pItem = PyList_GetItem(pList, i);
        long lit = PyLong_AsLong(pItem);
        v = abs(lit) - 1;
        while (v >= S->nVars())
            S->newVar();
        clause.push((lit > 0) ? mkLit(v) : ~mkLit(v));
    }

    S->addClause(clause);

    Py_RETURN_NONE;
}

PyObject *solve(PyObject *self, PyObject *args) {

    char *path;
    bool simplify, log, solve;
    lbool result;
    PyObject *pList;
    PyObject *pItem;
    vec<Lit> assumptions;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "bbbOs", &solve, &simplify, &log, &pList, &path)) {
        Py_RETURN_NONE;
    }

    if (log) {
        printHeader();
        S->log = true;
    } else {
        S->log = false;
    }

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        pItem = PyList_GetItem(pList, i);
        long lit = PyLong_AsLong(pItem);
        assumptions.push((lit > 0) ? mkLit(v) : ~mkLit(v));
    }

    for (i = 0; i < assumptions.size(); i++) {
        S->addClause(assumptions[i]);
    }

    assumptions.clear(true);

    if (strcmp(path, "") != 0) {
        S->toDimacs(path);
    }

    if (solve) {
        if (simplify) {
            S->eliminate();
            result = S->solveLimited(assumptions, true);
        } else {
            result = S->solveLimited(assumptions, false);
        }
    } else {
        return PyList_New(0);
    }

    if (S->log) {
        printf("\n");
    }

    if (result == l_True) {
        PyObject *modelList = PyList_New(S->nVars());
        if (result == l_True) {
            for (int i = 0; i < S->nVars(); i++)
                if (S->model[i] != l_Undef) {
                    PyList_SetItem(modelList, i, PyLong_FromLong((S->model[i] == l_True) ? +(i + 1) : -(i + 1)));
                }
        }
        S->model.clear(true);
        return modelList;
    }
    return PyList_New(0);
}

#endif //SLIME_SAT_SOLVER_SLIME_HH
