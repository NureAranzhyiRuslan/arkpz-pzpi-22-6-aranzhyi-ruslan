cmake_minimum_required(VERSION 3.29)
project(atark_iot)

set(CMAKE_CXX_STANDARD 23)

add_executable(atark_iot main.cpp)
target_link_libraries(atark_iot cpr)

# TODO: add cpr and toml++ in here with require_package