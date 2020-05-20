#include "ccadical.h"
#include <peqnp_sat.h>

extern "C" {

const char *peqnp_sat_description() { return ccadical_signature(); }

void *peqnp_sat_init() { return ccadical_init(); }

void peqnp_sat_add(void *solver, int lit) { ccadical_add((CCaDiCaL *) solver, lit); }

int peqnp_sat_val(void *solver, int lit) { return ccadical_val((CCaDiCaL *) solver, lit); }

int peqnp_sat_solve(void *solver) { return ccadical_solve((CCaDiCaL *) solver); }
}
