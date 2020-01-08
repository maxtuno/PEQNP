///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2018 Oscar Riveros. all rights reserved.        //
//                         oscar.riveros@peqnp.science                       //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <hess/hess.h>

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

void inv(struct cpu *box) {
    box->m = box->i;
    box->n = box->j;
    while (box->i < box->j) {
        box->cmp++;
        box->ram = box->seq[box->i];
        box->seq[box->i] = box->seq[box->j];
        box->seq[box->j] = box->ram;
        box->i++;
        box->j--;
    }
    box->i = box->m;
    box->j = box->n;
}

void hess(struct cpu *box) {
    box->sat = false;
    while (box->cmp++ < (box->len * box->len * box->len * box->len) && !box->sat) {
        o:
        for (box->l = 0; box->l < box->len * box->len && !box->sat; box->l++) {
            box->i = MIN(box->l / box->len, box->l % box->len);
            box->j = MAX(box->l / box->len, box->l % box->len);
            if (box->map[box->seq[!box->i ? box->len - 1 : box->i - 1]][box->seq[box->i]] + box->map[box->seq[!box->j ? box->len - 1 : box->j - 1]][box->seq[box->j]] <= 1) {
                oo:
                inv(box);
                box->loc = 0;
                for (box->k = 0; box->k < box->len - 1; box->k++) {
                    box->cmp++;
                    box->loc += !box->map[box->seq[box->k]][box->seq[box->k + 1]];
                    if (box->loc > box->glb) {
                        break;
                    }
                }
                if (box->loc < box->glb) {
                    box->glb = box->loc;
                    box->sat = !box->glb;
                    if (box->log) {
                        box->log(box);
                    }
                    goto o;
                } else if (box->loc > box->glb) {
                    goto oo;
                }
            }
        }
    }
}