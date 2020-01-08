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

struct cpu {
    I i;
    I j;
    I k;
    I l;
    I m;
    I n;
    I len;
    I loc;
    I glb;
    I ram;
    I cmp;
    I *seq;
    bool sat;
    bool **map;

    void (*log)(struct cpu *);
};

void hess(struct cpu *);

#ifdef __cplusplus
}
#endif

#endif //HCP_HESS_H
