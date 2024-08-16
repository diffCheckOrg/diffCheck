#include <gtest/gtest.h>
#include "diffCheck.hh"
#include "diffCheck/IOManager.hh"

//-------------------------------------------------------------------------
// fixtures
//-------------------------------------------------------------------------

class DFPointCloudTestFixture : public ::testing::Test {
protected:
    std::vector<Eigen::Vector3d> points;
    std::vector<Eigen::Vector3d> colors;
    std::vector<Eigen::Vector3d> normals;
    diffCheck::geometry::DFPointCloud dfPointCloud;

    DFPointCloudTestFixture() : dfPointCloud(points, colors, normals) {}

    void SetUp() override {
        dfPointCloud = diffCheck::geometry::DFPointCloud();
        std::string pathTest = diffCheck::io::GetRoofQuarterPlyPath();
        dfPointCloud.LoadFromPLY(diffCheck::io::GetRoofQuarterPlyPath());
    }

    void TearDown() override {
        // Clean up any resources if needed
    }
};

// add your fixtures here..

//-------------------------------------------------------------------------
// basic constructors
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, Constructor) {
    diffCheck::geometry::DFPointCloud dfPointCloud;
    EXPECT_EQ(dfPointCloud.GetNumPoints(), 0);
    EXPECT_EQ(dfPointCloud.GetNumColors(), 0);
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 0);
}

TEST_F(DFPointCloudTestFixture, ConstructorWithVectors) {
    std::vector<Eigen::Vector3d> points;
    std::vector<Eigen::Vector3d> colors;
    std::vector<Eigen::Vector3d> normals;
    diffCheck::geometry::DFPointCloud dfPointCloud(points, colors, normals);
    EXPECT_EQ(dfPointCloud.GetNumPoints(), 0);
    EXPECT_EQ(dfPointCloud.GetNumColors(), 0);
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 0);
}

//-------------------------------------------------------------------------
// i/o
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, LoadFromPLY) {
    EXPECT_EQ(dfPointCloud.GetNumPoints(), 7379);
    EXPECT_EQ(dfPointCloud.GetNumColors(), 7379);
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 7379);
}

//-------------------------------------------------------------------------
// properties
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, GetNumPoints){
    EXPECT_EQ(dfPointCloud.GetNumPoints(), 7379);
}

TEST_F(DFPointCloudTestFixture, GetNumColors) {
    EXPECT_EQ(dfPointCloud.GetNumColors(), 7379);
}

TEST_F(DFPointCloudTestFixture, GetNumNormals) {
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 7379);
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

//-------------------------------------------------------------------------
// converters
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, ConvertionO3dPointCloud) {
    std::shared_ptr<open3d::geometry::PointCloud> o3dPointCloud = dfPointCloud.Cvt2O3DPointCloud();
    std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloud2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
    dfPointCloud2->Cvt2DFPointCloud(o3dPointCloud);

    EXPECT_EQ(dfPointCloud.GetNumPoints(), dfPointCloud2->GetNumPoints());
    EXPECT_EQ(dfPointCloud.GetNumColors(), dfPointCloud2->GetNumColors());
    EXPECT_EQ(dfPointCloud.GetNumNormals(), dfPointCloud2->GetNumNormals());
}

TEST_F(DFPointCloudTestFixture, ConvertionCilantroPointCloud) {
    std::shared_ptr<cilantro::PointCloud3f> cilantroPointCloud = dfPointCloud.Cvt2CilantroPointCloud();
    std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloud2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
    dfPointCloud2->Cvt2DFPointCloud(cilantroPointCloud);

    EXPECT_EQ(dfPointCloud.GetNumPoints(), dfPointCloud2->GetNumPoints());
    EXPECT_EQ(dfPointCloud.GetNumColors(), dfPointCloud2->GetNumColors());
    EXPECT_EQ(dfPointCloud.GetNumNormals(), dfPointCloud2->GetNumNormals());
}

//-------------------------------------------------------------------------
// utilities
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, ComputeDistance) {
    std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloud2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
    dfPointCloud2->LoadFromPLY(diffCheck::io::GetRoofQuarterPlyPath());
    std::vector<double> distances = dfPointCloud.ComputeDistance(dfPointCloud2);
    EXPECT_EQ(distances.size(), 7379);
}

TEST_F(DFPointCloudTestFixture, ComputeAABB) {
    std::vector<Eigen::Vector3d> bbox = dfPointCloud.ComputeBoundingBox();
    EXPECT_EQ(bbox.size(), 2);
}

TEST_F(DFPointCloudTestFixture, ComputeOBB) {
    std::vector<Eigen::Vector3d> obb = dfPointCloud.GetTightBoundingBox();
    EXPECT_EQ(obb.size(), 8);
}

TEST_F(DFPointCloudTestFixture, EstimateNormals) {
    // knn
    dfPointCloud.EstimateNormals();
    EXPECT_EQ(dfPointCloud.GetNumNormals(), 7379);
    // radius
    dfPointCloud.EstimateNormals(false, 50, 0.1);
}

TEST_F(DFPointCloudTestFixture, ApplyColor) {
    dfPointCloud.ApplyColor(Eigen::Vector3d(1.0, 0.0, 0.0));
    for (int i = 0; i < dfPointCloud.GetNumColors(); i++) {
        EXPECT_EQ(dfPointCloud.Colors[i], Eigen::Vector3d(1.0, 0.0, 0.0));
    }
    dfPointCloud.ApplyColor(255, 0, 0);
    for (int i = 0; i < dfPointCloud.GetNumColors(); i++) {
        EXPECT_EQ(dfPointCloud.Colors[i], Eigen::Vector3d(1.0, 0.0, 0.0));
    }
}

//-------------------------------------------------------------------------
// Downsamplers
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, Downsample) {
    dfPointCloud.VoxelDownsample(0.1);
    std::cout << "after downsampling .. " << dfPointCloud.GetNumPoints() << std::endl;
    EXPECT_LT(dfPointCloud.GetNumPoints(), 7379);
    DFPointCloudTestFixture::SetUp();

    dfPointCloud.UniformDownsample(2);
    std::cout << "after downsampling .. " << dfPointCloud.GetNumPoints() << std::endl;
    EXPECT_LT(dfPointCloud.GetNumPoints(), 7379);
    DFPointCloudTestFixture::SetUp();

    dfPointCloud.DownsampleBySize(1000);
    std::cout << "after downsampling .. " << dfPointCloud.GetNumPoints() << std::endl;
    EXPECT_LT(dfPointCloud.GetNumPoints(), 1000);
    DFPointCloudTestFixture::SetUp();
}

//-------------------------------------------------------------------------
// Transformers
//-------------------------------------------------------------------------

TEST_F(DFPointCloudTestFixture, Transform) {
    Eigen::Matrix4d transformationMatrix = Eigen::Matrix4d::Identity();
    diffCheck::transformation::DFTransformation transformation = diffCheck::transformation::DFTransformation(transformationMatrix);
    dfPointCloud.ApplyTransformation(transformation);

    std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloud2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
    dfPointCloud2->LoadFromPLY(diffCheck::io::GetRoofQuarterPlyPath());
    dfPointCloud2->ApplyTransformation(transformation);

    std::vector<double> distances = dfPointCloud.ComputeDistance(dfPointCloud2);
    for (int i = 0; i < distances.size(); i++) {
        EXPECT_EQ(distances[i], 0);
    }
}

//-------------------------------------------------------------------------
// Others
//-------------------------------------------------------------------------