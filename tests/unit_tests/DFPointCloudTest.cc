#include <gtest/gtest.h>
#include "diffCheck.hh"

class DFPointCloudTestFixture : public ::testing::Test {
protected:
    std::vector<Eigen::Vector3d> points;
    std::vector<Eigen::Vector3d> colors;
    std::vector<Eigen::Vector3d> normals;
    diffCheck::geometry::DFPointCloud dfPointCloud;

    DFPointCloudTestFixture() : dfPointCloud(points, colors, normals) {}

    void SetUp() override {
        // Initialize your objects and variables here
        points = {Eigen::Vector3d(1, 2, 3)};
        colors = {Eigen::Vector3d(255, 255, 255)};
        normals = {Eigen::Vector3d(0, 0, 1)};

        // Reinitialize dfPointCloud in case you need to reset its state
        dfPointCloud = diffCheck::geometry::DFPointCloud(points, colors, normals);
    }

    void TearDown() override {
        // Clean up any resources if needed
    }
};

TEST_F(DFPointCloudTestFixture, GetNumPoints) {
    EXPECT_EQ(dfPointCloud.GetNumPoints(), 1);
}

TEST_F(DFPointCloudTestFixture, GetNumColors) {
    EXPECT_EQ(dfPointCloud.GetNumColors(), 1);
}

TEST_F(DFPointCloudTestFixture, GetNumNormals) {
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 1);
}

TEST_F(DFPointCloudTestFixture, HasPoints) {
    EXPECT_TRUE(dfPointCloud.HasPoints());
}

TEST_F(DFPointCloudTestFixture, HasColors) {
    EXPECT_TRUE(dfPointCloud.HasColors());
}

TEST_F(DFPointCloudTestFixture, HasNormals) {
    EXPECT_TRUE(dfPointCloud.HasNormals());
}

// int main(int argc, char **argv) {
//     ::testing::InitGoogleTest(&argc, argv);
//     return RUN_ALL_TESTS();
// }