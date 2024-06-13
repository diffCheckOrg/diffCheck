#include <gtest/gtest.h>
#include "diffCheck.hh"


TEST(DFPointCloudTest, TestConstructor) {
    std::vector<Eigen::Vector3d> points = {Eigen::Vector3d(1, 2, 3)};
    std::vector<Eigen::Vector3d> colors = {Eigen::Vector3d(255, 255, 255)};
    std::vector<Eigen::Vector3d> normals = {Eigen::Vector3d(0, 0, 1)};

    diffCheck::geometry::DFPointCloud dfPointCloud(points, colors, normals);

    // Verify that the points, colors, and normals are set correctly
    EXPECT_EQ(dfPointCloud.Points[0], points[0]);
    EXPECT_EQ(dfPointCloud.Colors[0], colors[0]);
    EXPECT_EQ(dfPointCloud.Normals[0], normals[0]);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}