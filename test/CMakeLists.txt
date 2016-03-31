cmake_minimum_required(VERSION 2.8.12)
project(MyCVODE)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(mycvode main.cpp)
target_link_libraries(mycvode ${CONAN_LIBS})
