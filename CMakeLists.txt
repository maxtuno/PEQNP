cmake_minimum_required(VERSION 2.8.12)
project(SLIME)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

include_directories(. include)

set(CMAKE_CXX_FLAGS "-std=c++11 -O3 -s -mtune=generic -Wno-unused-value -D NDEBUG -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS -D NO_PEQNP -D LOG")
add_executable(slime
        src/Main.cc
        src/SimpSolver.cc
        src/Solver.cc
        )
