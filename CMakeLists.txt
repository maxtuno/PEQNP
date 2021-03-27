cmake_minimum_required(VERSION 2.4)
project(SLIME)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

include_directories(. include)

find_package(MPI REQUIRED)
if (MPI_FOUND)
    set(CMAKE_CXX_COMPILER mpicxx)
    set(CMAKE_CXX_FLAGS "-std=c++11 -O3 -mtune=generic -Wno-unused-value -D NDEBUG -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS -D NO_PEQNP -D MASSIVE -D LOG")
    add_executable(slime
            src/Ls.cc
            src/Main.cc
            src/Options.cc
            src/SimpSolver.cc
            src/Solver.cc
            )
else(!MPI_FOUND)
    set(CMAKE_CXX_FLAGS "-std=c++11 -O3 -s -mtune=generic -Wno-unused-value -D NDEBUG -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS -D NO_PEQNP -D LOG")
    add_executable(slime
            src/Ls.cc
            src/Main.cc
            src/Options.cc
            src/SimpSolver.cc
            src/Solver.cc
            )
endif (MPI_FOUND)
