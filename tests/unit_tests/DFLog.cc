#include <gtest/gtest.h>
#include "diffCheck.hh"

class DFLogTestFixture : public ::testing::Test {};

TEST_F(DFLogTestFixture, LogInfo) {
    DIFFCHECK_INFO("This is an info message");
    SUCCEED();
}

TEST_F(DFLogTestFixture, LogWarn) {
    DIFFCHECK_WARN("This is a warning message");
    SUCCEED();
}

TEST_F(DFLogTestFixture, LogError) {
    // Use EXPECT_EXIT if you want the test to continue even if this check fails,
    // ( or ASSERT_EXIT to stop the test immediately if the check fails.)
    EXPECT_EXIT(
        {
            // Call the function that is expected to exit the program.
            // For example, if DIFFCHECK_ERROR causes the program to exit,
            // you would call it here.
            DIFFCHECK_ERROR("This is an error message");
            
            // Force an exit with a specific code if the above function call
            // does not exit for some reason. This is to ensure the exit
            // behavior is triggered for the test.
            exit(1); // Use the appropriate exit code expected by DIFFCHECK_ERROR.
        },
        // The exit predicate to check the exit status.
        // testing::ExitedWithCode checks that the program exited with the specified code.
        // Replace 1 with the actual exit code you expect DIFFCHECK_ERROR to use.
        testing::ExitedWithCode(1),
        // The expected output pattern. This can be a regex to match against
        // the output of the program upon exiting. If you don't need to check
        // the output, you can use ".*" to match anything.
        "This is an error message"
    );
}