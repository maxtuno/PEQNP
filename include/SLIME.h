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

#define DRAT // Generate unsat proof.

using namespace SLIME;

SimpSolver *S;
int v;

#if _WIN32 || _WIN64
#include <io.h>
#include <fcntl.h>
#include <windows.h>
void printHeader() {
    SetConsoleOutputCP(65001);
    std::cout << "                                         \n";
    std::cout << "   ██████  ██▓     ██▓ ███▄ ▄███▓▓█████  \n";
    std::cout << " ▒██    ▒ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▓█   ▀  \n";
    std::cout << " ░ ▓██▄   ▒██░    ▒██▒▓██    ▓██░▒███    \n";
    std::cout << "   ▒   ██▒▒██░    ░██░▒██    ▒██ ▒▓█  ▄  \n";
    std::cout << " ▒██████▒▒░██████▒░██░▒██▒   ░██▒░▒████▒ \n";
    std::cout << " ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░░░ ▒░ ░ \n";
    std::cout << " ░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░░  ░      ░ ░ ░  ░ \n";
    std::cout << " ░  ░  ░    ░ ░    ▒ ░░      ░      ░    \n";
    std::cout << "       ░      ░  ░ ░         ░      ░  ░ \n";
    std::cout << "                                         \n";
    std::cout << "           http://www.peqnp.com          \n";
    std::cout << "                                         \n";
}
#else

void printHeader() {
    printf("c                                         \n");
    printf("c   ██████  ██▓     ██▓ ███▄ ▄███▓▓█████  \n");
    printf("c ▒██    ▒ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▓█   ▀  \n");
    printf("c ░ ▓██▄   ▒██░    ▒██▒▓██    ▓██░▒███    \n");
    printf("c   ▒   ██▒▒██░    ░██░▒██    ▒██ ▒▓█  ▄  \n");
    printf("c ▒██████▒▒░██████▒░██░▒██▒   ░██▒░▒████▒ \n");
    printf("c ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░░░ ▒░ ░ \n");
    printf("c ░ ░▒  ░ ░░ ░ ▒  ░ ▒ ░░  ░      ░ ░ ░  ░ \n");
    printf("c ░  ░  ░    ░ ░    ▒ ░░      ░      ░    \n");
    printf("c       ░      ░  ░ ░         ░      ░  ░ \n");
    printf("c                                         \n");
    printf("c           http://www.peqnp.com          \n");
    printf("c                                         \n");
}

#endif

PyObject *slime_cli(PyObject *self, PyObject *args) {

    printHeader();

    char *cnf_path, *model_path, *proof_path;
    lbool result;

    if (!PyArg_ParseTuple(args, "sss", &cnf_path, &model_path, &proof_path)) {
        Py_RETURN_NONE;
    }

    SimpSolver slime;
    slime.log = true;

#ifdef DRAT
    slime.drup_file = fopen(proof_path, "wb");
#endif

    FILE *in = fopen(cnf_path, "r");
    if (in == NULL) {
        std::cout << "c ERROR! Could not open file: " << cnf_path << std::endl;
        Py_RETURN_NONE;
    }
    parse_DIMACS(in, slime);
    fclose(in);

    slime.eliminate();

    vec<Lit> assumptions;
    result = slime.solveLimited(assumptions);

    printf("\n");

    printf(result == l_True ? "s SATISFIABLE\nv " : result == l_False ? "s UNSATISFIABLE\n" : "s UNKNOWN\n");
    if (result == l_True) {
        for (int i = 0; i < slime.nVars(); i++)
            if (slime.model[i] != l_Undef) {
                printf("%s%s%d", (i == 0) ? "" : " ", (slime.model[i] == l_True) ? "" : "-", i + 1);
            }
        printf(" 0\n");
    } else {
#ifdef DRAT
        if (strcmp(proof_path, "") != 0) {
            fputc('a', slime.drup_file);
            fputc(0, slime.drup_file);
            fclose(slime.drup_file);
        }
#endif
    }

    if (strcmp(model_path, "") != 0) {
        FILE *model = fopen(model_path, "w");
        fprintf(model, result == l_True ? "SAT\n" : result == l_False ? "UNSAT\n" : "UNKNOWN\n");
        if (result == l_True) {
            for (int i = 0; i < slime.nVars(); i++)
                if (slime.model[i] != l_Undef) {
                    fprintf(model, "%s%s%d", (i == 0) ? "" : " ", (slime.model[i] == l_True) ? "" : "-", i + 1);
                }
            fprintf(model, " 0\n");
        }
    }

    if (result == l_True) {
        PyObject *modelList = PyList_New(slime.nVars());
        if (result == l_True) {
            for (int i = 0; i < slime.nVars(); i++)
                if (slime.model[i] != l_Undef) {
                    PyList_SetItem(modelList, i, PyLong_FromLong((slime.model[i] == l_True) ? +(i + 1) : -(i + 1)));
                }
        }
        return modelList;
    }

    return PyList_New(0);
}

PyObject *reset(PyObject *self, PyObject *args) {
    delete S;
    S = new SimpSolver();

    Py_RETURN_NONE;
}

PyObject *add_clause(PyObject *self, PyObject *args) {
    PyObject *pList;
    // Py_INCREF(pList);
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }

    vec<Lit> clause;

    n = PyList_Size(pList);
    for (i = 0; i < n; i++) {
        PyObject *pItem = PyList_GetItem(pList, i);
        // Py_INCREF(pItem);
        long lit = PyLong_AsLong(pItem);
        // Py_DECREF(pItem);
        v = (int)(abs(lit) - 1);
        while (v >= S->nVars())
            S->newVar();
        clause.push((lit > 0) ? mkLit(v) : ~mkLit(v));
    }
    // Py_DECREF(pList);

    S->addClause(clause);

    Py_RETURN_NONE;
}

PyObject *solve(PyObject *self, PyObject *args) {

    char *path, *model_path, *proof;
    bool simplify, log, solve;
    lbool result;
    PyObject *pList;
    PyObject *pItem;
    vec<Lit> assumptions;
    Py_ssize_t n;
    int i;

    if (!PyArg_ParseTuple(args, "bbbOsss", &solve, &simplify, &log, &pList, &path, &model_path, &proof)) {
        Py_RETURN_NONE;
    }

    S->render = strcmp(path, "") != 0;

    S->rank = 0;

    if (log) {
        S->log = true;
        if (S->simplify_ready) {
            printHeader();
        }
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

    if (strcmp(proof, "") != 0) {
        S->drup_file = fopen(proof, "wb");
    }

    if (solve) {
        if (simplify) {
            if (S->simplify_ready) {
                S->simplify_ready = false;
                S->eliminate();
            }
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

        if (strcmp(model_path, "") != 0) {
            FILE *model = fopen(model_path, "w");
            fprintf(model, result == l_True ? "SAT\n" : result == l_False ? "UNSAT\n" : "UNKNOWN\n");
            if (result == l_True) {
                for (int i = 0; i < S->nVars(); i++)
                    if (S->model[i] != l_Undef) {
                        fprintf(model, "%s%s%d", (i == 0) ? "" : " ", (S->model[i] == l_True) ? "" : "-", i + 1);
                    }
                fprintf(model, " 0\n");
            }
            fclose(model);
        }

        S->model.clear(true);

        return modelList;
    }

    if (strcmp(proof, "") != 0) {
        fputc('a', S->drup_file);
        fputc(0, S->drup_file);
        fclose(S->drup_file);
    }
    return PyList_New(0);
}

#endif //SLIME_SAT_SOLVER_SLIME_HH
