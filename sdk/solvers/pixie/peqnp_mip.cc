#include <peqnp_mip.h>
#include <pixie.hh>

const char *peqnp_mip_description() { return "PIXIE MIP Solver"; }

void *peqnp_mip_init() { return new pixie(); }

void peqnp_mip_set_objective(void *solver, double *objective, int size) {
    std::vector<double> objective_;
    objective_.assign(objective, objective + size);
    static_cast<pixie *>(solver)->add_objective(objective_);
}

void peqnp_mip_add_constraint(void *solver, double *constraint, int comparator, double right, int size) {
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
}

void peqnp_mip_set_integer_condition(void *solver, int *integer_condition, int size) {
    std::vector<bool> integer_condition_;
    integer_condition_.assign(integer_condition, integer_condition + size);
    static_cast<pixie *>(solver)->set_integer_condition(integer_condition_);
}

double peqnp_mip_maximize(void *solver) { return static_cast<pixie *>(solver)->optimize(); }

double peqnp_mip_val(void *solver, int idx) { return static_cast<pixie *>(solver)->get_variable(idx); }
