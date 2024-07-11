#include <gtest/gtest.h>

int add(int a, int b) {
    return a + b;
}

TEST(AddTest, HandlesPositiveInput) {
    EXPECT_EQ(6, add(2, 4));
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}