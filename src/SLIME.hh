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
    printf("                                         \n");
    printf("   ██████  ██▓     ██▓ ███▄ ▄███▓▓█████  \n");
    printf(" ▒██    ▒ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▓█   ▀  \n");
    printf(" ░ ▓██▄   ▒██░    ▒██▒▓██    ▓██░▒███    \n");
    printf("   ▒   ██▒▒██░    ░██░▒██    ▒██ ▒▓█  ▄  \n");
    printf(" ▒██████▒▒░██████▒░██░▒██▒   ░██▒░▒████▒ \n");
    printf(" ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░░░ ▒░ ░ \n");
    printf(" ░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░░  ░      ░ ░ ░  ░ \n");
    printf(" ░  ░  ░    ░ ░    ▒ ░░      ░      ░    \n");
    printf("       ░      ░  ░ ░         ░      ░  ░ \n");
    printf("                                         \n");
    printf("        http://www.slime.science         \n");
    printf("                                         \n");
}
#endif

PyObject *reset(PyObject *self, PyObject *args) {
    // printHeader();
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
        int lit = PyLong_AsLong(pItem);
        v = abs(lit) - 1;
        while (v >= S->nVars())
            S->newVar();
        clause.push((lit > 0) ? mkLit(v) : ~mkLit(v));
    }

    S->addClause(clause);

    Py_RETURN_NONE;
}

PyObject *solve(PyObject *self, PyObject *args) {

    bool simplify;
    if (!PyArg_ParseTuple(args, "b", &simplify)) {
        Py_RETURN_NONE;
    }

    if (simplify) {
        S->eliminate();
    }

    vec<Lit> assumptions;
    lbool result = S->solveLimited(assumptions, false);

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
