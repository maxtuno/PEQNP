///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

/*
 * PEQNP SAT SOLVER Interface.
 */

#ifndef PEQNP_SAT_H
#define PEQNP_SAT_H

/*
 * Version of the interface.
 */
#define VERSION 1

#if defined(_WIN32) || defined(__CYGWIN__)
#if defined(__GNUC__)
#define PEQNP_API __attribute__((dllexport))
#elif defined(_MSC_VER)
#define PEQNP_API __declspec(dllexport)
#endif
#else
#define PEQNP_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif
/*
 * Return a short arbitrary description of the solver.
 */
PEQNP_API const char *peqnp_sat_description();
/*
 * Initialize the system, and release resources if is call with a initialized system.
 * Return a pointer to the solver.
 */
PEQNP_API void *peqnp_sat_init();
/*
 * Add a literal to the current clause, when the literal is 0, the clauses is closed and add to the current cnf.
 * Need the pointer to the solver created with init, and a literal.
 */
PEQNP_API void peqnp_sat_add(void *solver, int literal);
/*
 * Solve the current added clauses.
 * Need the pointer to the solver created with init.
 */
PEQNP_API int peqnp_sat_solve(void *solver);
/*
 * Get the current polarity of literal.
 * Need the pointer to the solver created with init.
 */
PEQNP_API int peqnp_sat_val(void *solver, int literal);
#ifdef __cplusplus
}
#endif

#endif // PEQNP_SAT_H
