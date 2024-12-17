cmake_minimum_required(VERSION 3.29)
project(atark_iot)

set(CMAKE_CXX_STANDARD 23)

find_package(cpr REQUIRED)
find_package(tomlplusplus REQUIRED)

add_executable(atark_iot
        src/measurement_source.cpp
        src/iot_sensor.cpp
        src/main.cpp)
target_include_directories(atark_iot PRIVATE include)
target_link_libraries(atark_iot cpr)

if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(atark_iot PRIVATE -fPIC -fvisibility=hidden -Os -s -Wl,--gc-sections -flto=auto)
endif()
