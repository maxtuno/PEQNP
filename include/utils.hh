///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef MIP_SOLVER_UTILS_HH
#define MIP_SOLVER_UTILS_HH

#include <chrono>
#include <cmath>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <limits>
#include <fstream>


enum C {
    L,
    E,
    G,
};

#define EPS 1e-10

bool ii(const double x) { return (std::abs(x - round(x)) <= EPS); }

#endif // MIP_SOLVER_UTILS_HH
