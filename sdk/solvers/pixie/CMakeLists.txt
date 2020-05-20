cmake_minimum_required(VERSION 2.4)
project(PIXIE)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

include_directories(. include ../../mip)

set(CMAKE_CXX_FLAGS "-std=c++11 -Os -D NDEBUG")

add_library(PIXIE SHARED peqnp_mip.cc)