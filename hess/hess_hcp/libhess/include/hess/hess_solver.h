///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2018 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef HCP_HESS_H
#define HCP_HESS_H

#ifdef __cplusplus
extern "C" {
#else
#include <stdbool.h>
#endif

typedef unsigned long long int I;

struct box {
    I len;
    I loc;
    I glb;
    I ram;
    I *seq;
    bool sat;
    bool **map;

    void (*log)(struct box *);
};

void hess(struct box *);

#ifdef __cplusplus
}
#endif

#endif //HCP_HESS_H
