#ifndef _order_hpp_INCLUDED
#define _order_hpp_INCLUDED

namespace CaDiCaL {

struct res_smaller {
  Internal * internal;
  res_smaller (Internal * i) : internal (i) { }
  bool operator () (unsigned a, unsigned b);
};

typedef heap<res_smaller> OrderSchedule;

}

#endif
