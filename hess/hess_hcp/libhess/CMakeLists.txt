cmake_minimum_required(VERSION 3.10)
project(libhess C)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-Os -Wall")

include_directories(./include)

add_library(hess SHARED src/hess.c include/hess/hess.h)