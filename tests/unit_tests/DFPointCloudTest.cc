#include <filesystem>

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
        std::filesystem::path path = std::filesystem::path(__FILE__).parent_path();
        std::filesystem::path pathCloud = path / "test_data" / "cloud.ply";

        dfPointCloud = diffCheck::geometry::DFPointCloud();
        dfPointCloud.LoadFromPLY(pathCloud.string());
    }

    void TearDown() override {
        // Clean up any resources if needed
    }
};

TEST_F(DFPointCloudTestFixture, ConvertionO3dPointCloud) {
    std::shared_ptr<open3d::geometry::PointCloud> o3dPointCloud = dfPointCloud.Cvt2O3DPointCloud();
    std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloud2 = std::make_shared<diffCheck::geometry::DFPointCloud>();

    dfPointCloud2->Cvt2DFPointCloud(o3dPointCloud);

    EXPECT_EQ(dfPointCloud.GetNumPoints(), dfPointCloud2->GetNumPoints());
    EXPECT_EQ(dfPointCloud.GetNumColors(), dfPointCloud2->GetNumColors());
    EXPECT_EQ(dfPointCloud.GetNumNormals(), dfPointCloud2->GetNumNormals());
}

// TODO: cilantro cloud convertion test + new methods

TEST_F(DFPointCloudTestFixture, ComputeAABB) {
    std::vector<Eigen::Vector3d> bbox = dfPointCloud.ComputeBoundingBox();
    EXPECT_EQ(bbox.size(), 2);
}

TEST_F(DFPointCloudTestFixture, ComputeOBB) {
    std::vector<Eigen::Vector3d> obb = dfPointCloud.GetTightBoundingBox();
    EXPECT_EQ(obb.size(), 8);
}

TEST_F(DFPointCloudTestFixture, GetNumPoints){
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