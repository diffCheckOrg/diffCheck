
#include "diffCheck.hh"

#include <iostream>
#include <fstream>


int main()
{
  // import clouds
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_1 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtr_2 = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrWithoutNormals = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfPointCloudPtrGroundTruthFromMesh = std::make_shared<diffCheck::geometry::DFPointCloud>();
  std::shared_ptr<diffCheck::geometry::DFMesh> dfMeshPtr = std::make_shared<diffCheck::geometry::DFMesh>();
  std::shared_ptr<diffCheck::geometry::DFPointCloud> dfGroundTruth = std::make_shared<diffCheck::geometry::DFPointCloud>();

  // std::string pathCloud = R"(C:\Users\andre\Downloads\scan_data_normals.ply\scan_data_normals.ply)";
  // std::string pathMesh = R"(F:\diffCheck\assets\dataset\mesh_fromRh_unfixedLength.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  // create a sphere from o3d

  std::string pathCloud = R"(C:\Users\localuser\Downloads\00_pt.ply)";
  std::string pathMesh = R"(C:\Users\localuser\Downloads\00_mesh.ply)";
  // std::string pathMesh = R"(F:\diffCheck\temp\03_mesh.ply)";

  dfMeshPtr->LoadFromPLY(pathMesh);
  dfPointCloudPtr->LoadFromPLY(pathCloud);

  dfGroundTruth->Cvt2DFPointCloud(dfMeshPtr->Cvt2O3DTriangleMesh()->SamplePointsUniformly(10000));
  Eigen::Matrix4d transformation = Eigen::Matrix4d::Identity();
  transformation(0, 3) = 0.0;
  transformation(1, 3) = -0.02;
  transformation(2, 3) = 0.02;
  Eigen::Matrix3d rotation;
  rotation = Eigen::AngleAxisd(0, Eigen::Vector3d::UnitY());
  transformation.block<3, 3>(0, 0) = rotation * transformation.block<3, 3>(0, 0);

  dfPointCloudPtr->ApplyTransformation(transformation);

  diffCheck::transformation::DFTransformation localRegistration = diffCheck::registration::RefinedRegistration::O3DICP(dfPointCloudPtr, dfGroundTruth, 0.05);

  diffCheck::transformation::DFTransformation otherlocalRegistration = diffCheck::registration::RefinedRegistration::O3DGeneralizedICP(dfPointCloudPtr, dfGroundTruth, 0.05);
  dfPointCloudPtr->ApplyTransformation(localRegistration);

  std::cout<<localRegistration.TransformationMatrix<<std::endl;
  std::cout<<otherlocalRegistration.TransformationMatrix<<std::endl;
  
  std::shared_ptr<diffCheck::visualizer::Visualizer> vis = std::make_shared<diffCheck::visualizer::Visualizer>();
  // vis->AddPointCloud(dfPointCloudPtr);
  vis->AddMesh(dfMeshPtr);
  vis->AddPointCloud(dfGroundTruth);
  vis->AddPointCloud(dfPointCloudPtr);
  vis->Run();
  return 0;
}