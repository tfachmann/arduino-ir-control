cmake_minimum_required(VERSION 3.0.0)

project(arduino_ir_control CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(arduino_ir_control main.cpp)
target_link_arduino_libraries(arduino_ir_control PRIVATE IRremote core)
target_enable_arduino_upload(arduino_ir_control)
