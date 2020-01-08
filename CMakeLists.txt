cmake_minimum_required(VERSION 2.8)
project(slime)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

add_subdirectory(${PROJECT_SOURCE_DIR}/hess/cvrpt)
add_subdirectory(${PROJECT_SOURCE_DIR}/hess/hess_hcp)
add_subdirectory(${PROJECT_SOURCE_DIR}/hess/hess_max2sat)

include_directories(. include)

set(CMAKE_CXX_FLAGS "-std=c++98 -O3 -D NDEBUG -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS -D LOG") # -static

add_executable(slime_cli
        src/Main.cc
        src/SimpSolver.cc
        src/Solver.cc
        )

