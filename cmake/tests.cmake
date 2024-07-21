include(CTest)
include(external_tools)

enable_testing()
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/deps/googletest)
set(TESTS_OUT_DIR ${CMAKE_BINARY_DIR}/df_tests/)
set(TEST_OUT_DIR_BINARY ${TESTS_OUT_DIR}/${CMAKE_BUILD_TYPE})

# ------------------------------------------------------------------------------
# c++
# ------------------------------------------------------------------------------
# add new test suites .cc here
# FIXME: change the name to SUITE_TEST
set(CPP_UNIT_TESTS df_unit_tests)
add_executable(${CPP_UNIT_TESTS}
    tests/unit_tests/DFPointCloudTest.cc
    tests/unit_tests/DFLog.cc
    tests/allCppTests.cc
    )
set_target_properties(${CPP_UNIT_TESTS} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${TESTS_OUT_DIR}
    )
target_link_libraries(${CPP_UNIT_TESTS} gtest gtest_main)
target_link_libraries(${CPP_UNIT_TESTS} ${SHARED_LIB_NAME})

add_test(NAME ${CPP_UNIT_TESTS} COMMAND ${CPP_UNIT_TESTS})
copy_dlls(${TEST_OUT_DIR_BINARY} ${CPP_UNIT_TESTS})

# ------------------------------------------------------------------------------
# Python
# ------------------------------------------------------------------------------
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

set(PYTEST_FILE ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests/test_pybind_units.py)
add_test(NAME PYBIND_UNIT_TESTS
         COMMAND ${PYTHON_EXECUTABLE} -m pytest ${PYTEST_FILE}
         WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
         )
# here we need to copy the dlls and the pyd file to the pypi directory

# ------------------------------------------------------------------------------
# Run all tests
# ------------------------------------------------------------------------------
# FIXME: the post build has some problems if the tests are failing MSB3073
if (RUN_TESTS)
    add_custom_command(
                    TARGET ${UNIT_TESTS}  #TODO: <== this should be set to the latest test suite
                    POST_BUILD
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                    COMMAND ${CMAKE_CTEST_COMMAND} -C $<CONFIGURATION> --output-on-failures --verbose
                    COMMENT "Running all tests"
                 )
endif()