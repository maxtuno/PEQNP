#include <peqnp_mip.h>
#include <pixie.hh>

PEQNP_API const char *peqnp_mip_description() { return "PIXIE MIP Solver"; }

PEQNP_API void *peqnp_mip_init() { return new pixie(); }

PEQNP_API void *peqnp_mip_set_objective(void *solver, double *objective, int size) {
    std::vector<double> objective_;
    objective_.assign(objective, objective + size);
    static_cast<pixie *>(solver)->add_objective(objective_);
    return solver;
}

PEQNP_API void *peqnp_mip_add_constraint(void *solver, double *constraint, int comparator, double right, int size) {
    std::vector<double> constraint_;
    constraint_.assign(constraint, constraint + size);
    std::string cmp;
    if (comparator < 0) {
        cmp = "<=";
    }
    if (comparator == 0) {
        cmp = "==";
    }
    if (comparator > 0) {
        cmp = ">=";
    }
    static_cast<pixie *>(solver)->add_constraint(constraint_, cmp, right);
    return solver;
}

PEQNP_API void *peqnp_mip_set_integer_condition(void *solver, int *integer_condition, int size) {
    std::vector<bool> integer_condition_;
    integer_condition_.assign(integer_condition, integer_condition + size);
    static_cast<pixie *>(solver)->set_integer_condition(integer_condition_);
    return solver;
}

PEQNP_API double peqnp_mip_maximize(void *solver) { return static_cast<pixie *>(solver)->optimize(); }

PEQNP_API double peqnp_mip_val(void *solver, int idx) { return static_cast<pixie *>(solver)->get_variable(idx); }

#if _WIN32 || _WIN64
#include <Python.h>
PyMODINIT_FUNC PyInit_PIXIE() { Py_RETURN_NONE; }
#endif