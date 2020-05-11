///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef MIP_SOLVER_RESULT_HH
#define MIP_SOLVER_RESULT_HH

#include "utils.hh"

struct result {
    double z{};
    std::vector<double> x{};

    result() = default;

    explicit result(const unsigned int size) {
        z = -std::numeric_limits<double>::max();
        x.resize(size);
    }

    double get_optimal() {
        return z;
    }

    std::vector<double> get_variables() {
        return x;
    }
};

#endif // MIP_SOLVER_RESULT_HH
