cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)

include(CTest)
enable_testing()

set(BUILD_SHARED_LIBS ON)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

file(GLOB_RECURSE SOURCES src/*.cc src/*.hh)

add_executable(${PROJECT_NAME} ${SOURCES})

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

target_include_directories(${PROJECT_NAME}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )


#--------------------------------------------------------------------------
# Pre-compiled headers
#--------------------------------------------------------------------------
target_precompile_headers(${PROJECT_NAME} PRIVATE src/diffcheckpch.hh)