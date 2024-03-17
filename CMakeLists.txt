cmake_minimum_required(VERSION 3.16.)
project(DiffCheck VERSION 1.0.0 LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(external_tools)


#--------------------------------------------------------------------------
# options
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# library
#--------------------------------------------------------------------------


set(SHARED_LIB_NAME diffCheck)

file(GLOB_RECURSE SOURCES_LIB 
    src/diffCheck.cc src/diffCheck.hh        # diffCheck interface
    src/diffCheck/*.cc src/diffCheck/*.hh    # diffCheck src
    src/diffcheckpch.cc src/diffcheckpch.hh  # precompiled headers
    )

add_library(${SHARED_LIB_NAME} SHARED ${SOURCES_LIB})

if (WIN32)
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        WINDOWS_EXPORT_ALL_SYMBOLS TRUE
        )
endif()
    set_target_properties(${SHARED_LIB_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin  # for dll
        # ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin  # for lib
        )

target_include_directories(${SHARED_LIB_NAME}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )

target_precompile_headers(${SHARED_LIB_NAME} PUBLIC src/diffcheckpch.hh)


#--------------------------------------------------------------------------
# executable
#--------------------------------------------------------------------------

set(APP_NAME_EXE diffCheckApp)

add_executable(${APP_NAME_EXE} src/diffCheckApp.cc)

set_target_properties(${APP_NAME_EXE} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )

target_link_libraries(${APP_NAME_EXE} ${SHARED_LIB_NAME})

target_include_directories(${APP_NAME_EXE}
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
    )

#--------------------------------------------------------------------------
# Pre-compiled headers
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Tests
#--------------------------------------------------------------------------

include(CTest)
enable_testing()

# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests/global_registrations)