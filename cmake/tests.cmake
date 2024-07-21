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

# copying pyd and dlls
set(TARGET_PYBIND_TESTS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests)
add_custom_command(TARGET ${PYBINDMODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PYBINDMODULE_NAME}>
        ${TARGET_PYBIND_TESTS_DIR}
        )
copy_dlls(${TARGET_PYBIND_TESTS_DIR} ${PYBINDMODULE_NAME})

add_test(NAME PYBIND_UNIT_TEST
         COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests/test_pybind_units.py
         WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
         )
add_test(NAME PYBIND_PYVER_TEST
         COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_tests/pybinds_tests/test_pybind_pyver.py
         WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
         )

# ------------------------------------------------------------------------------
# Run all tests
# ------------------------------------------------------------------------------
# FIXME: the post build has some problems if the tests are failing MSB3073
if (RUN_TESTS)
    add_custom_command(
                    TARGET ${CPP_UNIT_TESTS} POST_BUILD  #TODO: <== this should be set to the latest test suite
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                    COMMAND ${CMAKE_CTEST_COMMAND} -C $<CONFIGURATION> --output-on-failures --verbose
                    COMMENT "Running all tests"
                 )
endif()