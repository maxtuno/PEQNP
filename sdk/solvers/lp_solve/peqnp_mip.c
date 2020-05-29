#include <lp_lib.h>
#include <peqnp_mip.h>

REAL *var;
int done = 0;

/*
 * Return a short arbitrary description of the solver.
 */
PEQNP_API const char *peqnp_mip_description() { return "LP_SOLVE Mixed Integer Linear Programming solver"; }
/*
 * Initialize the system, and release resources if is call with a initialized system.
 * Return a pointer to the solver.
 */
PEQNP_API void *peqnp_mip_init() {
    done = 0;
    if (var) {
        free(var);
    }
    lprec *solver = make_lp(0, 0);
    set_verbose(solver, NEUTRAL);
    return solver;
}
/*
 * ax + by + cx
 * Set the objective of the current problem.
 * Need the pointer to the solver created with init,
 * The coefficients for the objective and the size of objective array.
 */
PEQNP_API void *peqnp_mip_set_objective(void *solver, double *objective, int size) {
    var = (REAL *)calloc(size, sizeof(REAL));
    int *colno = (int *)calloc(size, sizeof(int));
    for (int i = 0; i < size; i++) {
        colno[i] = i + 1;
    }
    set_obj_fnex((lprec *)solver, size, objective, colno);
    return solver;
}
/*
 * ax + by + cx <= d
 * Add constraint to current problem.
 * Need the pointer to the solver created with init,
 * The coefficients for the left side of constraint,
 * A integer representing a comparator -1 <=, 0 ==, 1 >=,
 * The right number of the constraint and the size of the coefficients.
 */
PEQNP_API void *peqnp_mip_add_constraint(void *solver, double *constraint, int comparator, double right, int size) {
    if (!done) {
        delete_lp(solver);
        solver = make_lp(0, size);
        set_verbose(solver, NEUTRAL);
        done = 1;
    }
    int *colno = (int *)calloc(size, sizeof(int));
    for (int i = 0; i < size; i++) {
        colno[i] = i + 1;
    }
    // set_add_rowmode((lprec *)solver, TRUE);
    if (comparator < 0) {
        add_constraintex((lprec *)solver, size, constraint, colno, LE, right);
    }
    if (comparator == 0) {
        add_constraintex((lprec *)solver, size, constraint, colno, EQ, right);
    }
    if (comparator > 0) {
        add_constraintex((lprec *)solver, size, constraint, colno, GE, right);
    }
    // set_add_rowmode((lprec *)solver, FALSE);
    return solver;
}
/*
 * Set when a variable is integer or double.
 * Need the pointer to the solver created with init,
 * An array of ints with 0 if is double, or 1 if its integer.
 * The size of the array.
 */
PEQNP_API void *peqnp_mip_set_integer_condition(void *solver, int *integer_condition, int size) {
    for (int i = 0; i < size; i++) {
        set_int(solver, i + 1, integer_condition[i]);
    }
    return solver;
}
/*
 * Maximize the current objective
 * Need the pointer to the solver created with init,
 * NOTE: PEQNP use the symmetry to solve problems with Minimize.
 */
PEQNP_API double peqnp_mip_maximize(void *solver) {
    set_maxim((lprec *)(solver));
    solve((lprec *)(solver));
    return get_objective((lprec *)(solver));
}
/*
 * Get the current value of a variable by index.
 * Need the pointer to the solver created with init,
 */
PEQNP_API double peqnp_mip_val(void *solver, int idx) {
    get_variables((lprec *)solver, var);
    return var[idx];
}

#if _WIN32 || _WIN64
#include <Python.h>
PyMODINIT_FUNC PyInit_LPSOLVE() { Py_RETURN_NONE; }
#endif