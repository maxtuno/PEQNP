/*------------------------------------------------------------------------*/

// We prefer short 3 character version numbers made of digits and lower case
// letters only, which gives 36^3 = 46656 different versions.  The following
// macro is used for the non-standard build process and only set from
// the file '../VERSION' with '../scripts/update-version.sh'.  The standard
// build process relies on 'VERSION' to be defined in 'build.hpp'.

#  define VERSION "1.2.1"

/*------------------------------------------------------------------------*/

// The copyright of the code is here.

static const char * COPYRIGHT =
"Copyright (c) 2016-2019 Armin Biere, JKU Linz"
;

/*------------------------------------------------------------------------*/

// Again if we do not have 'NBUILD' or if something during configuration is
// broken we still want to be able to compile the solver.  In this case we
// then try our best to figure out 'COMPILER' and 'DATE', but for
// 'IDENTIFIER' and 'FLAGS' we can only use the '0' string, which marks
// those as unknown.

#ifndef COMPILER
#  ifdef __clang__
#    ifdef __VERSION__
#      define COMPILER "clang++-" __VERSION__
#    else
#      define COMPILER "clang++"
#    endif
#  elif defined (__GNUC__)
#    ifdef __VERSION__
#      define COMPILER "g++-" __VERSION__
#    else
#      define COMPILER "g++"
#    endif
#  else
#    define COMPILER 0
#  endif
#endif

// GIT SHA2 identifier.
//
#ifndef IDENTIFIER
#  define IDENTIFIER 0
#endif

// Compilation flags.
//
#ifndef FLAGS
#  define FLAGS 0
#endif

// Build Time and operating system.
//
#ifndef DATE
#  define DATE __DATE__ __TIME__
#endif

/*------------------------------------------------------------------------*/

#include "version.hpp"

namespace CaDiCaL {

const char * version () { return VERSION; }
const char * copyright () { return COPYRIGHT; }
const char * signature () { return "cadical-" VERSION; }
const char * identifier () { return IDENTIFIER; }
const char * compiler () { return COMPILER; }
const char * date () { return DATE; }
const char * flags () { return FLAGS; }

}
