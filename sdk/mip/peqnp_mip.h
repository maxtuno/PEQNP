///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

/*
 * PEQNP MIP SOLVER Interface.
 */

#ifndef PEQNP_MIP_H
#define PEQNP_MIP_H

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
PEQNP_API const char *peqnp_mip_description();
/*
 * Initialize the system, and release resources if is call with a initialized system.
 * Return a pointer to the solver.
 */
PEQNP_API void *peqnp_mip_init();
/*
 * ax + by + cx
 * Set the objective of the current problem.
 * Need the pointer to the solver created with init,
 * The coefficients for the objective and the size of objective array.
 */
PEQNP_API void peqnp_mip_set_objective(void *solver, double *objective, int size);
/*
 * ax + by + cx <= d
 * Add constraint to current problem.
 * Need the pointer to the solver created with init,
 * The coefficients for the left side of constraint,
 * A integer representing a comparator -1 <=, 0 ==, 1 >=,
 * The right number of the constraint and the size of the coefficients.
 */
PEQNP_API void peqnp_mip_add_constraint(void *solver, double *constraint, int comparator, double right, int size);
/*
 * Set when a variable is integer or double.
 * Need the pointer to the solver created with init,
 * An array of ints with 0 if is double, or 1 if its integer.
 * The size of the array.
 */
PEQNP_API void peqnp_mip_set_integer_condition(void *solver, int *integer_condition, int size);
/*
 * Maximize the current objective
 * Need the pointer to the solver created with init,
 * NOTE: PEQNP use the symmetry to solve problems with Minimize.
 */
PEQNP_API double peqnp_mip_maximize(void *solver);
/*
 * Get the current value of a variable by index.
 * Need the pointer to the solver created with init,
 */
PEQNP_API double peqnp_mip_val(void *solver, int idx);
#ifdef __cplusplus
}
#endif

#endif // PEQNP_MIP_H
