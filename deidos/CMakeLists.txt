cmake_minimum_required(VERSION 3.9)
project(peqnp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-Os -mtune=generic -lstdc++ -Wall")

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-Os -mtune=generic -Wall")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

find_package(Boost)
if (Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIR})
    add_executable(deidos_covenant_boost deidos_covenant_boost.cpp)
endif()

add_executable(deidos_covenant deidos_covenant.cpp)