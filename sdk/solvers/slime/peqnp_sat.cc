#include "Solver.h"
#include <cstdlib>

using namespace SLIME;

extern "C" {
static const char *sig = "SLIME SAT Solver";

class PEQNP_SAT : public Solver {
    vec<Lit> clause;
    bool nomodel;

    Lit import(int lit) {
        while (abs(lit) > nVars())
            (void)newVar();
        return mkLit(Var(abs(lit) - 1), (lit < 0));
    }

  public:
    void add(int lit) {
        nomodel = true;
        if (lit)
            clause.push(import(lit));
        else
            addClause(clause), clause.clear();
    }

    int solve() {
        vec<Lit> assumptions;
        lbool res = solveLimited(assumptions);
        nomodel = (res != l_True);
        return (res == l_Undef) ? 0 : (res == l_True ? 10 : 20);
    }

    int val(int lit) {
        if (nomodel)
            return 0;
        lbool res = modelValue(import(lit));
        return (res == l_True) ? lit : -lit;
    }
};
}

extern "C" {
#include <peqnp_sat.h>
static PEQNP_SAT *import(void *s) { return (PEQNP_SAT *)s; }
const char *peqnp_sat_description() { return sig; }
void *peqnp_sat_init() { return new PEQNP_SAT(); }
void peqnp_sat_add(void *s, int l) { import(s)->add(l); }
int peqnp_sat_solve(void *s) { return import(s)->solve(); }
int peqnp_sat_val(void *s, int l) { return import(s)->val(l); }
};

#if _WIN32 || _WIN64
#include <Python.h>
PyMODINIT_FUNC PyInit_SLIME() { Py_RETURN_NONE; }
#endif
