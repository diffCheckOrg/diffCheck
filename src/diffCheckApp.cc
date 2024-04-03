
#include "diffCheck.hh"

#include <open3d/Open3D.h>
#include <open3d/io/PointCloudIO.h>
#include <open3d/io/TriangleMeshIO.h>
#include <open3d/visualization/visualizer/Visualizer.h>

#include <iostream>


int main()
{
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterTrans = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrAfterReg = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();

  std::string pathCloud = R"(C:\Users\localuser\Downloads\04_pt.ply)";
  std::string pathMesh = R"(C:\Users\localuser\Downloads\04_mesh.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  dfMeshPtr->LoadFromPLY(pathMesh);
  dfPointCloudPtr->LoadFromPLY(pathCloud);

  // populate the mesh with points and store it in dfPointCloudPtrGroundTruth
  dfPointCloudPtrGroundTruth->Cvt2DFPointCloud(dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(100000));

  // create a rigid rotation matrix
  Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
  T.block<3, 3>(0, 0) = Eigen::AngleAxisd(3 , Eigen::Vector3d::UnitZ()).toRotationMatrix(); // Yes, Pi = 3 in this world
  T(0, 3) = 10;
  T(1, 3) = -40;

  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudAfterTrans = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtr->Cvt2O3DPointCloud()->Transform(T));
  dfPointCloudPtrAfterTrans->Cvt2DFPointCloud(o3DPointCloudAfterTrans);

  std::shared_ptr<diffCheck::registration::Registration> reg = std::make_shared<diffCheck::registration::Registration>();
  //auto result = reg->O3DFastGlobalRegistrationFeatureMatching(dfPointCloudPtrAfterTrans, dfPointCloudPtr);
  auto result = reg->O3DFastGlobalRegistrationBasedOnCorrespondence(dfPointCloudPtrAfterTrans, dfPointCloudPtr);

  // apply the transformation to the source point cloud
  Eigen::Matrix<double, 4, 4> transformation = result.transformation_;
  std::shared_ptr<open3d::geometry::PointCloud> o3DPointCloudPtrAfterReg = std::make_shared<open3d::geometry::PointCloud>(dfPointCloudPtrAfterTrans->Cvt2O3DPointCloud()->Transform(transformation));
  dfPointCloudPtrAfterReg->Cvt2DFPointCloud(o3DPointCloudPtrAfterReg);
  std::vector<double> errors = reg->ComputeP2PDistance(dfPointCloudPtrAfterReg, dfPointCloudPtrGroundTruth);
  std::cout << "Mean distance: " << std::accumulate(errors.begin(), errors.end(), 0.0) / errors.size() << std::endl;

  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  vis->AddPointCloud(dfPointCloudPtrGroundTruth);
  vis->AddPointCloud(dfPointCloudPtrAfterReg);
  vis->AddMesh(dfMeshPtr);
  vis->Run();

  return 0;
}