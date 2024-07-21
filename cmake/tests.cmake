include(CTest)
include(external_tools)

enable_testing()
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/deps/googletest)
set(TESTS_OUT_DIR ${CMAKE_BINARY_DIR}/df_tests/)
set(TEST_OUT_DIR_BINARY ${TESTS_OUT_DIR}/${CMAKE_BUILD_TYPE})

# add new test suites .cc here
# FIXME: change the name to SUITE_TEST
set(UNIT_TESTS df_test_suites)
add_executable(${UNIT_TESTS}
    tests/unit_tests/DFPointCloudTest.cc
    tests/unit_tests/DFLog.cc
    tests/allTests.cc
    )
set_target_properties(${UNIT_TESTS} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${TESTS_OUT_DIR}
    )
target_link_libraries(${UNIT_TESTS} gtest gtest_main)
target_link_libraries(${UNIT_TESTS} ${SHARED_LIB_NAME})

add_test(NAME ${UNIT_TESTS} COMMAND ${UNIT_TESTS})
copy_dlls(${TEST_OUT_DIR_BINARY} ${UNIT_TESTS})

# check if the tests should be run


# FIXME: the post build has some problems if the tests are failing MSB3073
# wether or not to run the tests
set(EXE_TESTS_NAME ${TEST_OUT_DIR_BINARY}/${UNIT_TESTS}.exe)
if (RUN_TESTS)
    # message(STATUS "Running tests..")
    # add_custom_target(run_tests
    #     COMMAND ${UNIT_TESTS}
    #     DEPENDS ${UNIT_TESTS}
    #     )
    add_custom_command(
                   TARGET ${UNIT_TESTS}
                   POST_BUILD
                #    COMMAND ${EXE_TESTS_NAME}
                #    WORKING_DIRECTORY ${TEST_OUT_DIR_BINARY}
                   WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                   COMMAND ${CMAKE_CTEST_COMMAND} -C $<CONFIGURATION> -R "^${UNIT_TESTS}$" --output-on-failures
                   COMMENT "Running ${UNIT_TESTS} after build")
endif()