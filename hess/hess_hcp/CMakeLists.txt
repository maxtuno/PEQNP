cmake_minimum_required(VERSION 3.10)
project(hcp CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-Os -Wall -mtune=native")

include_directories(libhess/include /usr/local/include)
link_directories(libhess/lib /usr/local/lib)

add_executable(hp hp.cpp)
target_link_libraries(hp hess)

add_subdirectory(libhess)

add_executable(hp_gui hp_gui.cpp)
target_link_libraries(hp_gui hess SDL2)